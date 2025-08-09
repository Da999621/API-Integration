#!/usr/bin/env python3
"""
API Integration Script
Fetches and displays weather data and cryptocurrency prices from external APIs
Handles errors gracefully and provides user-friendly output
"""

import requests
import json
from datetime import datetime

class APIIntegration:
    """Main class for handling API integrations"""
    
    def __init__(self):
        self.weather_api_key = "demo_key"  # Replace with actual API key
        self.weather_base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.crypto_base_url = "https://api.coingecko.com/api/v3"
        
    def fetch_weather_data(self, city_name):
        """
        Fetch weather data for a given city
        
        Args:
            city_name (str): Name of the city
            
        Returns:
            dict: Weather information or None if error
        """
        try:
            # Build API URL
            params = {
                'q': city_name,
                'appid': self.weather_api_key,
                'units': 'metric'
            }
            
            response = requests.get(self.weather_base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                weather_info = {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'weather_description': data['weather'][0]['description'].title(),
                    'wind_speed': data['wind']['speed'],
                    'visibility': data.get('visibility', 'N/A'),
                    'timestamp': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
                }
                
                return weather_info
            else:
                print(f"Error: Unable to fetch weather data (Status code: {response.status_code})")
                return None
                
        except requests.exceptions.Timeout:
            print("Error: Request timed out. Please check your internet connection.")
            return None
        except requests.exceptions.ConnectionError:
            print("Error: Failed to connect to weather API. Please check your internet connection.")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    
    def fetch_crypto_prices(self, crypto_symbols):
        """
        Fetch cryptocurrency prices
        
        Args:
            crypto_symbols (list): List of cryptocurrency symbols (e.g., ['bitcoin', 'ethereum'])
            
        Returns:
            dict: Cryptocurrency prices or None if error
        """
        try:
            # Convert symbols to IDs for CoinGecko API
            ids = ','.join(crypto_symbols)
            url = f"{self.crypto_base_url}/simple/price"
            params = {
                'ids': ids,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                crypto_info = {}
                for symbol in crypto_symbols:
                    if symbol in data:
                        crypto_info[symbol] = {
                            'price': data[symbol]['usd'],
                            'change_24h': data[symbol].get('usd_24h_change', 0),
                            'market_cap': data[symbol].get('usd_market_cap', 'N/A'),
                            'volume_24h': data[symbol].get('usd_24h_vol', 'N/A')
                        }
                
                return crypto_info
            else:
                print(f"Error: Unable to fetch crypto data (Status code: {response.status_code})")
                return None
                
        except requests.exceptions.Timeout:
            print("Error: Request timed out. Please check your internet connection.")
            return None
        except requests.exceptions.ConnectionError:
            print("Error: Failed to connect to crypto API. Please check your internet connection.")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    
    def display_weather(self, weather_data):
        """Display weather data in a user-friendly format"""
        if not weather_data:
            return
            
        print("\n" + "="*50)
        print("🌤️  WEATHER INFORMATION")
        print("="*50)
        print(f"Location: {weather_data['city']}, {weather_data['country']}")
        print(f"Temperature: {weather_data['temperature']}°C")
        print(f"Feels Like: {weather_data['feels_like']}°C")
        print(f"Description: {weather_data['weather_description']}")
        print(f"Humidity: {weather_data['humidity']}%")
        print(f"Pressure: {weather_data['pressure']} hPa")
        print(f"Wind Speed: {weather_data['wind_speed']} m/s")
        print(f"Visibility: {weather_data['visibility']} meters")
        print(f"Last Updated: {weather_data['timestamp']}")
    
    def display_crypto_prices(self, crypto_data):
        """Display cryptocurrency prices in a user-friendly format"""
        if not crypto_data:
            return
            
        print("\n" + "="*50)
        print("CRYPTOCURRENCY PRICES")
        print("="*50)
        
        for symbol, data in crypto_data.items():
            print(f"\n{symbol.upper()}:")
            print(f"  Price: ${data['price']:,.2f}")
            print(f"  24h Change: {data['change_24h']:+.2f}%")
            if data['market_cap'] != 'N/A':
                print(f"  Market Cap: ${data['market_cap']:,.0f}")
            if data['volume_24h'] != 'N/A':
                print(f"  24h Volume: ${data['volume_24h']:,.0f}")

def main():
    """Main function to run the API integration"""
    api = APIIntegration()
    
    print("🚀 API Integration Script")
    print("Fetching data from external APIs...")
    
    # Fetch weather data
    city = input("\nEnter city name for weather data (e.g., London, New York): ").strip()
    if city:
        weather_data = api.fetch_weather_data(city)
        api.display_weather(weather_data)
    
    # Fetch crypto prices
    print("\nFetching cryptocurrency prices...")
    crypto_symbols = ['bitcoin', 'ethereum', 'cardano', 'solana']
    crypto_data = api.fetch_crypto_prices(crypto_symbols)
    api.display_crypto_prices(crypto_data)
    
    # Interactive mode
    while True:
        print("\n" + "="*50)
        print("Choose an option:")
        print("1. Check weather for another city")
        print("2. Check specific cryptocurrency")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == '1':
            city = input("Enter city name: ").strip()
            if city:
                weather_data = api.fetch_weather_data(city)
                api.display_weather(weather_data)
        
        elif choice == '2':
            crypto = input("Enter cryptocurrency name (e.g., bitcoin, ethereum): ").strip().lower()
            if crypto:
                crypto_data = api.fetch_crypto_prices([crypto])
                api.display_crypto_prices(crypto_data)
        
        elif choice == '3':
            print("Thank you for using API Integration Script!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
