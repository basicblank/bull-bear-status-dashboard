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
        params = {
            'vs_currency': vs_currency,
            'days': days
        }

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)

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
        timeframe_map = {
            '4H': '4H',
            '6H': '6H',
            '12H': '12H',
            '1D': '1D',
            '2D': '2D',
            '3D': '3D',
            '1W': '1W'
        }

        if timeframe not in timeframe_map:
            return df

        resampled = df.resample(timeframe_map[timeframe]).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last'
        }).dropna()

        return resampled