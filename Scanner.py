import time
import requests

# CONFIGURATION PARAMETERS
ODDS_API_KEY = 'f4d35efa9891beef9b72344e501ddac3'
YOUR_MATRIX_WEBHOOK = https://cee-app-1.onrender.com

# WHALE TRIGGER THRESHOLDS
MIN_GAP_THRESHOLD = 25 # Trigger if the Money Handle/Bets gap is wide

def scan_whale_signals():
    print("🔄 Starting automated betting matrix scan...")
    try:
        # 1. Fetch upcoming NFL and NHL markets from Odds-API
        url = "https://the-odds-api.com"
        params = {
            'apiKey': ODDS_API_KEY,
            'regions': 'us',
            'markets': 'totals,spreads',
            'oddsFormat': 'american'
        }
        
        response = requests.get(url, params=params)
        games = response.json()
        detected_moves = []
        
        # 2. Package data and send to your web layout
        if games:
            print(f"📦 Sending updated data payload to matrix dashboard...")
            # For testing/initialization, we send the structured payload to the webhook
            # (The server will accept and display this live data dynamically)
            requests.post(YOUR_MATRIX_WEBHOOK, json=games)
            
    except Exception as e:
        print(f"❌ Error during automation scan: {str(e)}")

if __name__ == "__main__":
    scan_whale_signals()
