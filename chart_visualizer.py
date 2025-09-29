import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st

class ChartVisualizer:
    def __init__(self):
        self.colors = {
            'bullish': '#00D4AA',
            'bearish': '#FF6B6B',
            'neutral': '#FFA726',
            'candle_up': '#00D4AA',
            'candle_down': '#FF6B6B',
            'ema_12': '#2196F3',
            'ema_21': '#FF9800',
            'volume': 'rgba(158,158,158,0.3)'
        }

    def create_price_chart(self, df: pd.DataFrame, crypto_name: str, analysis: dict, timeframe: str):
        """Create an interactive price chart with trend analysis"""

        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxis=True,
            vertical_spacing=0.05,
            row_heights=[0.8, 0.2],
            subplot_titles=(f'{crypto_name} - {timeframe}', 'Volume')
        )

        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='Price',
                increasing_line_color=self.colors['candle_up'],
                decreasing_line_color=self.colors['candle_down'],
                showlegend=False
            ),
            row=1, col=1
        )

        # Add EMAs if available
        if 'EMA_12' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['EMA_12'],
                    mode='lines',
                    name='EMA 12',
                    line=dict(color=self.colors['ema_12'], width=2),
                    opacity=0.8
                ),
                row=1, col=1
            )

        if 'EMA_21' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['EMA_21'],
                    mode='lines',
                    name='EMA 21',
                    line=dict(color=self.colors['ema_21'], width=2),
                    opacity=0.8
                ),
                row=1, col=1
            )

        # Add trend annotations
        self._add_trend_annotations(fig, df, analysis)

        # Volume bars (if volume data is available)
        if 'volume' in df.columns:
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df['volume'],
                    name='Volume',
                    marker_color=self.colors['volume'],
                    showlegend=False
                ),
                row=2, col=1
            )

        # Update layout
        fig.update_layout(
            title=dict(
                text=f'{crypto_name} Price Chart - {analysis["trend"]} Trend',
                x=0.5,
                font=dict(size=20)
            ),
            xaxis_rangeslider_visible=False,
            height=700,
            template='plotly_white',
            hovermode='x unified'
        )

        # Update axes
        fig.update_xaxes(
            title_text="Date",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)'
        )

        fig.update_yaxes(
            title_text="Price (USD)",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            row=1, col=1
        )

        fig.update_yaxes(
            title_text="Volume",
            showgrid=False,
            row=2, col=1
        )

        return fig

    def _add_trend_annotations(self, fig, df, analysis):
        """Add trend analysis annotations to the chart"""
        last_price = df['close'].iloc[-1]
        trend_color = self.colors['bullish'] if analysis['trend'] == 'BULLISH' else self.colors['bearish'] if analysis['trend'] == 'BEARISH' else self.colors['neutral']

        # Add trend status annotation
        fig.add_annotation(
            x=df.index[-1],
            y=last_price,
            text=f"{analysis['trend']}<br>Strength: {analysis['strength']:.2f}",
            showarrow=True,
            arrowhead=2,
            arrowcolor=trend_color,
            bgcolor=trend_color,
            bordercolor='white',
            font=dict(color='white', size=12),
            opacity=0.9
        )

        # Add crossover signals
        if 'EMA_12' in df.columns and 'EMA_21' in df.columns:
            ema_12 = df['EMA_12']
            ema_21 = df['EMA_21']

            # Find recent crossovers
            crossovers = self._find_crossovers(ema_12, ema_21)

            for i, (cross_type, cross_date) in enumerate(crossovers[-5:]):  # Last 5 crossovers
                if cross_date in df.index:
                    price_at_cross = df.loc[cross_date, 'close']
                    color = self.colors['bullish'] if cross_type == 'bullish' else self.colors['bearish']
                    symbol = '▲' if cross_type == 'bullish' else '▼'

                    fig.add_annotation(
                        x=cross_date,
                        y=price_at_cross,
                        text=symbol,
                        showarrow=False,
                        font=dict(color=color, size=20),
                        bgcolor='white',
                        bordercolor=color,
                        borderwidth=2
                    )

    def _find_crossovers(self, ema_short, ema_long):
        """Find EMA crossover points"""
        crossovers = []

        for i in range(1, len(ema_short)):
            if (ema_short.iloc[i-1] <= ema_long.iloc[i-1] and
                ema_short.iloc[i] > ema_long.iloc[i]):
                crossovers.append(('bullish', ema_short.index[i]))
            elif (ema_short.iloc[i-1] >= ema_long.iloc[i-1] and
                  ema_short.iloc[i] < ema_long.iloc[i]):
                crossovers.append(('bearish', ema_short.index[i]))

        return crossovers

    def create_trend_heatmap(self, trend_data: dict, timeframes: list):
        """Create a trend heatmap showing all cryptocurrencies across timeframes"""

        cryptos = list(trend_data.keys())

        # Create matrix for heatmap
        z_values = []
        hover_text = []

        for crypto in cryptos:
            row_values = []
            row_hover = []

            for tf in timeframes:
                if tf in trend_data[crypto]:
                    trend = trend_data[crypto][tf]['trend']
                    strength = trend_data[crypto][tf]['strength']

                    # Convert trend to numeric value for heatmap
                    if trend == 'BULLISH':
                        value = strength
                        color_text = f"🐂 {trend}"
                    elif trend == 'BEARISH':
                        value = -strength
                        color_text = f"🐻 {trend}"
                    else:
                        value = 0
                        color_text = f"⚖️ {trend}"

                    row_values.append(value)
                    row_hover.append(f"{crypto}<br>{tf}<br>{color_text}<br>Strength: {strength:.2f}")
                else:
                    row_values.append(0)
                    row_hover.append(f"{crypto}<br>{tf}<br>No Data")

            z_values.append(row_values)
            hover_text.append(row_hover)

        fig = go.Figure(data=go.Heatmap(
            z=z_values,
            x=timeframes,
            y=cryptos,
            text=hover_text,
            texttemplate="%{text}",
            textfont={"size": 10},
            colorscale=[
                [0, self.colors['bearish']],
                [0.5, self.colors['neutral']],
                [1, self.colors['bullish']]
            ],
            zmid=0,
            hoverongaps=False,
            showscale=True,
            colorbar=dict(
                title="Trend Strength",
                titleside="right",
                tickvals=[-1, 0, 1],
                ticktext=["Bearish", "Neutral", "Bullish"]
            )
        ))

        fig.update_layout(
            title="Crypto Trend Heatmap Across Timeframes",
            xaxis_title="Timeframe",
            yaxis_title="Cryptocurrency",
            height=400,
            template='plotly_white'
        )

        return fig