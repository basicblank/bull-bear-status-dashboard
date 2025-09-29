import requests
import pandas as pd
import os
from dotenv import load_dotenv
from typing import Dict, List, Optional
import time

load_dotenv()

class CoinGeckoAPI:
    def __init__(self):
        self.api_key = os.getenv('COINGECKO_API_KEY')
        self.base_url = 'https://api.coingecko.com/api/v3'
        self.pro_url = 'https://pro-api.coingecko.com/api/v3'
        self.session = requests.Session()

        if self.api_key:
            self.session.headers.update({'X-Cg-Pro-Api-Key': self.api_key})
            self.base_url = self.pro_url

    def get_historical_data(self, coin_id: str, vs_currency: str = 'usd', days: int = 30) -> pd.DataFrame:
        """Get historical OHLC data for a cryptocurrency"""
        endpoint = f"{self.base_url}/coins/{coin_id}/ohlc"

        # CoinGecko OHLC API limits: 1, 7, 14, 30, 90, 180, 365
        # Map requested days to valid API values
        valid_days = [1, 7, 14, 30, 90, 180, 365]
        api_days = min([d for d in valid_days if d >= days], default=365)

        params = {
            'vs_currency': vs_currency,
            'days': api_days
        }

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if not data:
                print(f"No data returned for {coin_id}")
                return pd.DataFrame()

            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)

            # Convert to numeric types
            for col in ['open', 'high', 'low', 'close']:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            return df

        except requests.RequestException as e:
            print(f"Error fetching data for {coin_id}: {e}")
            return pd.DataFrame()

    def get_market_data(self, coin_ids: List[str], vs_currency: str = 'usd') -> Dict:
        """Get current market data for multiple cryptocurrencies"""
        endpoint = f"{self.base_url}/simple/price"
        params = {
            'ids': ','.join(coin_ids),
            'vs_currencies': vs_currency,
            'include_24hr_change': 'true',
            'include_24hr_vol': 'true'
        }

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching market data: {e}")
            return {}

    def resample_data(self, df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """Resample OHLC data to different timeframes"""
        if df.empty:
            return pd.DataFrame()

        timeframe_map = {
            '4H': '4h',
            '6H': '6h',
            '12H': '12h',
            '1D': '1D',
            '2D': '2D',
            '3D': '3D',
            '1W': '1W'
        }

        if timeframe not in timeframe_map:
            return df

        try:
            # Check if DataFrame has datetime index
            if not isinstance(df.index, pd.DatetimeIndex):
                print(f"Error: DataFrame must have DatetimeIndex for resampling")
                return pd.DataFrame()

            resampled = df.resample(timeframe_map[timeframe]).agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last'
            }).dropna()

            # Ensure we have enough data for analysis
            if len(resampled) < 25:  # Need at least 25 periods for EMA calculation
                print(f"Warning: Only {len(resampled)} periods for {timeframe}, may not be sufficient")

            return resampled
        except Exception as e:
            print(f"Error resampling {timeframe}: {e}")
            return pd.DataFrame()
