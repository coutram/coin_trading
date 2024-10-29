import random

import os
import datetime
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")

# Alchemy API setup
BASE_URL = f"https://solana-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"


def get_memecoin_data():
    # For simplicity, simulate data fetching
    return [
        {
            'name': 'Memecoin1',
            'price': round(random.uniform(0.01, 1.0), 4),
            'volume_change': round(random.uniform(0, 300), 2),
        },
        {
            'name': 'Memecoin2',
            'price': round(random.uniform(0.01, 1.0), 4),
            'volume_change': round(random.uniform(0, 300), 2),
        },
    ]


# Define time range for the last 30 days
def get_thirty_days_ago_iso():
    thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    return thirty_days_ago.isoformat()

# Fetch transactions for a specific token address
def fetch_transactions(token_address, from_time):
    url = f"{BASE_URL}/getAssetTransfers"
    params = {
        "fromBlock": from_time,
        "toBlock": "latest",
        "contractAddresses": [token_address],
        "category": ["token"]
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {token_address}: {response.status_code}")
        return None

# Analyze wallet activity
def analyze_wallet_activity(transfers):
    wallet_activity = {}
    for txn in transfers.get('transfers', []):
        wallet = txn.get('from')
        value = txn.get('value', 0)
        if wallet not in wallet_activity:
            wallet_activity[wallet] = {
                "volume": 0,
                "count": 0
            }
        wallet_activity[wallet]["volume"] += value
        wallet_activity[wallet]["count"] += 1
    return wallet_activity

# Fetch data for multiple memecoin addresses
def get_top_performing_wallets():
    memecoin_addresses = [
        "MemecoinTokenAddress1",
        "MemecoinTokenAddress2",
        # Add more memecoin token addresses
    ]
    from_time = get_thirty_days_ago_iso()
    total_activity = {}

    for address in memecoin_addresses:
        data = fetch_transactions(address, from_time)
        if data:
            wallet_activity = analyze_wallet_activity(data)
            for wallet, activity in wallet_activity.items():
                if wallet not in total_activity:
                    total_activity[wallet] = activity
                else:
                    total_activity[wallet]["volume"] += activity["volume"]
                    total_activity[wallet]["count"] += activity["count"]

    # Sort wallets by volume
    sorted_wallets = sorted(total_activity.items(), key=lambda x: x[1]['volume'], reverse=True)
    print("Top Performing Wallets in the Last 30 Days:")
    for i, (wallet, activity) in enumerate(sorted_wallets[:10]):
        print(f"{i + 1}. Wallet: {wallet}, Volume: {activity['volume']}, Transactions: {activity['count']}")
