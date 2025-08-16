# project_5_webscraping_regex_pandas.py

import requests
import pandas as pd
import time
import os
from datetime import datetime

# Define API endpoint
API_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"

# Define output path
OUTPUT_DIR = os.path.join(os.getcwd(), "Crypto_Data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_bitcoin_price():
    """
    Fetch Bitcoin price data from Coindesk API
    """
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        price_usd = data["bpi"]["USD"]["rate_float"]

        return {"timestamp": timestamp, "price_usd": price_usd}

    except Exception as e:
        print(f"⚠️ Error fetching data: {e}")
        return None

def save_to_csv(record):
    """
    Append new record to CSV file
    """
    file_path = os.path.join(OUTPUT_DIR, "bitcoin_prices.csv")

    # If file exists, append; otherwise, create new DataFrame
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])

    df.to_csv(file_path, index=False)
    print(f"✅ Data saved at {record['timestamp']}")

def run_scraper(interval=60, iterations=5):
    """
    Run scraper at set intervals (default: every 60s for 5 iterations)
    """
    print(f"🚀 Starting scraper: {iterations} runs every {interval} seconds...")
    for i in range(iterations):
        record = fetch_bitcoin_price()
        if record:
            save_to_csv(record)
        time.sleep(interval)

if __name__ == "__main__":
    # Example: scrape every 30s for 3 times
    run_scraper(interval=30, iterations=3)
