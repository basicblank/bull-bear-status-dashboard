import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta

from coingecko_api import CoinGeckoAPI
from trend_analyzer import TrendAnalyzer
from chart_visualizer import ChartVisualizer

# For Streamlit Cloud secrets
if hasattr(st, 'secrets') and 'COINGECKO_API_KEY' in st.secrets:
    import os
    os.environ['COINGECKO_API_KEY'] = st.secrets['COINGECKO_API_KEY']

# Page configuration
st.set_page_config(
    page_title="Crypto Bull/Bear Status",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize API and analyzer
@st.cache_resource
def initialize_components():
    api = CoinGeckoAPI()
    analyzer = TrendAnalyzer()
    visualizer = ChartVisualizer()
    return api, analyzer, visualizer

api, analyzer, visualizer = initialize_components()

# Cryptocurrency configuration
CRYPTOS = {
    'Bitcoin': 'bitcoin',
    'Ethereum': 'ethereum',
    'Solana': 'solana'
}

TIMEFRAMES = ['4H', '6H', '12H', '1D', '2D', '3D', '1W']

# Title and description
st.title("📈 Crypto Bull/Bear Status Dashboard")
st.markdown("**Track bullish and bearish trends across major cryptocurrencies**")

# Sidebar controls
st.sidebar.header("⚙️ Settings")

# API Key input (for local development)
if not api.api_key:  # Only show if no API key is set
    api_key_input = st.sidebar.text_input(
        "CoinGecko API Key (Optional - Pro features)",
        type="password",
        help="Enter your CoinGecko Pro API key for enhanced features"
    )

    if api_key_input:
        api.api_key = api_key_input
        api.session.headers.update({'X-Cg-Pro-Api-Key': api_key_input})
        api.base_url = api.pro_url
else:
    st.sidebar.success("🔑 API Key Connected!")

# Timeframe selection
selected_timeframe = st.sidebar.selectbox(
    "Select Timeframe",
    TIMEFRAMES,
    index=3  # Default to 1D
)

# Data refresh interval
auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)", value=False)

# Manual refresh button
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()

# Days of historical data based on timeframe
# CoinGecko API: ≤30 days = hourly data, >30 days = daily data
timeframe_days = {
    '4H': 30,    # 30 days = ~180 hourly periods → 4H resampling
    '6H': 30,    # 30 days = ~180 hourly periods → 6H resampling
    '12H': 30,   # 30 days = ~180 hourly periods → 12H resampling
    '1D': 90,    # 90 days = ~90 daily periods → 1D resampling
    '2D': 365,   # 365 days = ~365 daily periods → 2D resampling (~180 periods)
    '3D': 365,   # 365 days = ~365 daily periods → 3D resampling (~120 periods)
    '1W': 365    # 365 days = ~365 daily periods → 1W resampling (~52 periods)
}

days = timeframe_days.get(selected_timeframe, 30)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_crypto_data(crypto_id, days, timeframe):
    """Fetch and process cryptocurrency data"""
    try:
        df = api.get_historical_data(crypto_id, days=days)
        if df.empty:
            st.warning(f"No historical data available for {crypto_id}")
            return None, None

        # Resample data to selected timeframe
        resampled_df = api.resample_data(df, timeframe)

        if resampled_df.empty:
            st.warning(f"No data available for {crypto_id} at {timeframe} timeframe. Try a different timeframe.")
            return None, None

        # Check if we have enough data for EMA calculation
        if len(resampled_df) < 25:
            st.warning(f"Insufficient data for {crypto_id} at {timeframe} timeframe ({len(resampled_df)} periods). Need at least 25 periods for reliable EMA analysis.")
            return None, None

        # Analyze trends
        trend_analysis = analyzer.get_overall_trend(resampled_df)

        return resampled_df, trend_analysis
    except Exception as e:
        st.error(f"Error fetching data for {crypto_id}: {e}")
        return None, None

# Main dashboard
col1, col2, col3 = st.columns(3)

# Function to get trend color and emoji
def get_trend_display(trend, strength):
    if trend == 'BULLISH':
        color = "🟢"
        emoji = "🐂"
    elif trend == 'BEARISH':
        color = "🔴"
        emoji = "🐻"
    else:
        color = "🟡"
        emoji = "⚖️"

    return color, emoji

# Display data for each cryptocurrency
columns = [col1, col2, col3]
crypto_names = list(CRYPTOS.keys())

for i, (crypto_name, crypto_id) in enumerate(CRYPTOS.items()):
    with columns[i]:
        st.subheader(f"{crypto_name}")

        # Create placeholder for loading
        placeholder = st.empty()

        with placeholder.container():
            with st.spinner(f"Loading {crypto_name} data..."):
                df, analysis = fetch_crypto_data(crypto_id, days, selected_timeframe)

            if df is not None and analysis is not None:
                # Current price
                current_price = df['close'].iloc[-1]
                price_change = ((df['close'].iloc[-1] - df['close'].iloc[-2]) / df['close'].iloc[-2]) * 100

                # Trend display
                color, emoji = get_trend_display(analysis['trend'], analysis['strength'])

                # Display metrics
                st.metric(
                    label=f"Current Price",
                    value=f"${current_price:,.2f}",
                    delta=f"{price_change:+.2f}%"
                )

                st.markdown(f"""
                **{emoji} Trend Status: {color} {analysis['trend']}**

                **Strength:** {analysis['strength']:.2f}

                **EMA Analysis:**
                - 📈 EMA 12: ${analysis['ema_12_value']:.2f}
                - 📊 EMA 21: ${analysis['ema_21_value']:.2f}
                - 🔄 Position: {'EMA 12 > EMA 21' if analysis['ema_12_above_21'] else 'EMA 12 < EMA 21'}
                - ⚡ Recent Cross: {'🟢 Bullish' if analysis['recent_bullish_cross'] else '🔴 Bearish' if analysis['recent_bearish_cross'] else '⚪ None'}
                {f"- 📅 Crossover: {analysis['crossover_periods_ago']} periods ago" if analysis['crossover_periods_ago'] else ''}
                """)

                # Signal strength visualization
                strength_bars = int(analysis['strength'] * 5)  # Convert to 0-5 scale
                signal_color = "🟢" if analysis['trend'] == 'BULLISH' else "🔴" if analysis['trend'] == 'BEARISH' else "🟡"
                signal_text = signal_color * strength_bars + "⚪" * (5 - strength_bars)
                st.markdown(f"**Signal Strength:** {signal_text}")

                # Add chart toggle
                if st.button(f"📊 Show Chart", key=f"chart_{crypto_name}"):
                    chart = visualizer.create_price_chart(df, crypto_name, analysis, selected_timeframe)
                    st.plotly_chart(chart, use_container_width=True)

            else:
                st.error(f"Failed to load data for {crypto_name}")
                st.markdown("Please check your internet connection or API key.")

# Summary section
st.markdown("---")
st.subheader(f"📊 Summary - {selected_timeframe} Timeframe")

# Fetch all data for summary
summary_data = []
for crypto_name, crypto_id in CRYPTOS.items():
    df, analysis = fetch_crypto_data(crypto_id, days, selected_timeframe)
    if analysis:
        summary_data.append({
            'Crypto': crypto_name,
            'Trend': analysis['trend'],
            'Strength': f"{analysis['strength']:.2f}",
            'EMA 12': f"${analysis['ema_12_value']:.2f}",
            'EMA 21': f"${analysis['ema_21_value']:.2f}",
            'Recent Cross': 'Bullish' if analysis['recent_bullish_cross'] else 'Bearish' if analysis['recent_bearish_cross'] else 'None'
        })

if summary_data:
    summary_df = pd.DataFrame(summary_data)

    # Add trend emojis
    trend_emojis = {'BULLISH': '🐂', 'BEARISH': '🐻', 'NEUTRAL': '⚖️'}
    summary_df['Status'] = summary_df['Trend'].map(trend_emojis) + ' ' + summary_df['Trend']

    # Display summary table
    st.dataframe(
        summary_df[['Crypto', 'Status', 'Strength', 'EMA 12', 'EMA 21', 'Recent Cross']],
        use_container_width=True,
        hide_index=True
    )

# Auto refresh functionality
if auto_refresh:
    time.sleep(30)
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
**Methodology:**
- **EMA 12/21 Crossover:** Simple and effective trend following system
  - **Bullish:** When EMA 12 > EMA 21 (faster EMA above slower EMA)
  - **Bearish:** When EMA 12 < EMA 21 (faster EMA below slower EMA)
- **Trend Strength:** Based on crossover recency and EMA positioning
- **Signal Quality:** Higher strength for recent crossovers (within 1-2 periods)

*Data provided by CoinGecko API*
""")

# Display last update time
st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
