# 📈 Crypto Bull/Bear Status Dashboard

A Streamlit desktop application that analyzes and displays bullish/bearish trends for Bitcoin, Ethereum, and Solana across multiple timeframes using technical analysis.

## 🚀 Features

- **Multi-Timeframe Analysis**: 4H, 6H, 12H, 1D, 2D, 3D, and 1W timeframes
- **Dual Analysis Methods**:
  - Higher Highs/Higher Lows vs Lower Highs/Lower Lows structure analysis
  - EMA 12/21 crossover signals
- **Real-time Data**: Powered by CoinGecko API
- **Interactive Charts**: Plotly-based visualizations with trend annotations
- **Auto-refresh**: Optional 30-second data refresh
- **Trend Summary**: Comprehensive dashboard view

## 📋 Requirements

- Python 3.7+
- CoinGecko API key (optional but recommended for better rate limits)

## 🛠️ Installation

1. **Clone or download the project files to your desired directory**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your CoinGecko API key (optional):**
   ```bash
   cp .env.example .env
   # Edit .env and add your API key:
   COINGECKO_API_KEY=your_api_key_here
   ```

## 🎯 Usage

### Quick Start
```bash
python run.py
```

### Manual Start
```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## 📊 How It Works

### Trend Analysis Methods

1. **Market Structure Analysis**
   - Identifies swing highs and swing lows
   - Determines if recent structure shows:
     - Higher Highs + Higher Lows = Bullish Structure
     - Lower Highs + Lower Lows = Bearish Structure

2. **EMA Crossover Analysis**
   - Uses 12-period and 21-period Exponential Moving Averages
   - Bullish when EMA 12 > EMA 21
   - Bearish when EMA 12 < EMA 21
   - Tracks recent crossover events

### Trend Determination
- Combines both analysis methods
- Weights recent crossovers more heavily
- Calculates overall trend strength (0-1 scale)
- Provides clear BULLISH/BEARISH/NEUTRAL signals

## 🎮 Dashboard Features

### Main View
- **Three-column layout** for Bitcoin, Ethereum, and Solana
- **Current price** with 24h change percentage
- **Trend status** with emoji indicators (🐂/🐻/⚖️)
- **Signal strength** visualization
- **Detailed analysis breakdown**

### Interactive Elements
- **Timeframe selector** (sidebar)
- **Auto-refresh toggle** (30-second intervals)
- **Manual refresh button**
- **API key input** (for pro features)
- **Expandable charts** for each cryptocurrency

### Summary Table
- **Cross-asset overview** at selected timeframe
- **Trend comparison** across all cryptocurrencies
- **Signal strength metrics**

## 🔧 Configuration

### Supported Cryptocurrencies
- Bitcoin (BTC)
- Ethereum (ETH)
- Solana (SOL)

### Available Timeframes
- 4H, 6H, 12H (Short-term)
- 1D, 2D, 3D (Medium-term)
- 1W (Long-term)

### API Configuration
- **Free tier**: 10-50 calls/minute (sufficient for basic usage)
- **Pro tier**: Higher rate limits, recommended for frequent updates
- **Auto-fallback**: Works without API key using free tier

## 📈 Technical Indicators

- **EMA 12/21**: Exponential Moving Average crossover system
- **Swing Points**: Automated high/low identification
- **Trend Strength**: Quantified confidence measure
- **Signal Aggregation**: Multi-method consensus scoring

## 🎨 Visual Elements

- **Color coding**: Green (bullish), Red (bearish), Yellow (neutral)
- **Emoji indicators**: 🐂 Bull, 🐻 Bear, ⚖️ Neutral
- **Signal bars**: Visual strength representation
- **Interactive charts**: Candlesticks with EMA overlays
- **Trend annotations**: Crossover markers and labels

## 🔍 Troubleshooting

### Common Issues

1. **"Failed to load data"**
   - Check internet connection
   - Verify API key (if using)
   - Try refreshing the data

2. **Slow loading**
   - Use a CoinGecko Pro API key for better rate limits
   - Reduce auto-refresh frequency

3. **Charts not displaying**
   - Ensure all dependencies are installed
   - Try refreshing the browser

### Performance Tips
- Use API key for better rate limits
- Close unused browser tabs
- Restart the app if it becomes sluggish

## 🌟 Future Enhancements

- Additional cryptocurrencies
- More technical indicators (RSI, MACD, Bollinger Bands)
- Alert system for trend changes
- Historical performance tracking
- Portfolio integration
- Mobile-responsive design

## 📝 License

This project is for educational and personal use. Please respect CoinGecko's API terms of service.

## 🤝 Contributing

Feel free to fork, modify, and enhance this dashboard for your own use!

---

**Disclaimer**: This tool is for educational purposes only. Not financial advice. Always do your own research before making investment decisions.