import pandas as pd
import numpy as np
from typing import Dict

class TrendAnalyzer:
    def __init__(self):
        self.ema_short_period = 12
        self.ema_long_period = 21

    def calculate_ema(self, data: pd.Series, period: int) -> pd.Series:
        """Calculate Exponential Moving Average"""
        return data.ewm(span=period, adjust=False).mean()

    def analyze_ema_crossover(self, df: pd.DataFrame) -> Dict[str, any]:
        """Analyze EMA 12/21 crossover patterns"""
        ema_12 = self.calculate_ema(df['close'], self.ema_short_period)
        ema_21 = self.calculate_ema(df['close'], self.ema_long_period)

        # Add EMAs to dataframe for visualization
        df['EMA_12'] = ema_12
        df['EMA_21'] = ema_21

        # Check current positioning (EMA 12 above or below EMA 21)
        current_bullish = ema_12.iloc[-1] > ema_21.iloc[-1]

        # Check for recent crossover (within last 5 periods)
        recent_cross_bull = False
        recent_cross_bear = False
        crossover_periods_ago = None

        if len(ema_12) >= 2:
            for i in range(1, min(6, len(ema_12))):
                if (ema_12.iloc[-i-1] <= ema_21.iloc[-i-1] and
                    ema_12.iloc[-i] > ema_21.iloc[-i]):
                    recent_cross_bull = True
                    crossover_periods_ago = i
                    break
                elif (ema_12.iloc[-i-1] >= ema_21.iloc[-i-1] and
                      ema_12.iloc[-i] < ema_21.iloc[-i]):
                    recent_cross_bear = True
                    crossover_periods_ago = i
                    break

        # Determine trend based on EMA positioning
        if current_bullish:
            trend = 'BULLISH'
            trend_strength = 0.8 if recent_cross_bull else 0.6
        else:
            trend = 'BEARISH'
            trend_strength = 0.8 if recent_cross_bear else 0.6

        # Increase strength if crossover is very recent
        if crossover_periods_ago and crossover_periods_ago <= 2:
            trend_strength = min(1.0, trend_strength + 0.2)

        return {
            'trend': trend,
            'strength': trend_strength,
            'ema_12_value': ema_12.iloc[-1],
            'ema_21_value': ema_21.iloc[-1],
            'ema_12_above_21': current_bullish,
            'recent_bullish_cross': recent_cross_bull,
            'recent_bearish_cross': recent_cross_bear,
            'crossover_periods_ago': crossover_periods_ago,
            'price_above_ema12': df['close'].iloc[-1] > ema_12.iloc[-1],
            'price_above_ema21': df['close'].iloc[-1] > ema_21.iloc[-1]
        }

    def get_overall_trend(self, df: pd.DataFrame) -> Dict[str, any]:
        """Get trend analysis based solely on EMA 12/21 crossover"""
        return self.analyze_ema_crossover(df)