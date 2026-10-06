import time
import requests

# 1. SET YOUR TARGET URL
# Use 'http://127.0.0' for local testing
# Or use your live production link: 'https://onrender.com'
TARGET_URL = "http://127.0.0"

# 2. CONSTRUCT THE REAL-TIME 45-17 LIVE GAME DATA PAYLOAD
live_payload = {
    "slate": {
        "game": "Atlanta Falcons @ New Orleans Saints",
        "live_clock": "4TH QTR - LIVE",
        "score_string": "ATL 45 - 17 NO",
        "closing_line": 47.5,
        "sim_total": 62,
        "pacing_status": "Pacing 💥 OVER"
    },
    "players": [
        {
            "name": "Alvin Kamara",
            "position": "RB",
            "target": "Over 4.5 Live Receptions Floor (5 REC - CLEARED)",
            "is_floor": True
        },
        {
            "name": "Chris Olave",
            "position": "WR",
            "target": "Under 6.5 Live Receptions Ceiling (5 REC - ACTIVE)",
            "is_floor": False
        }
    ],
    "morale": [
        {
            "unit": "Saints O-Line",
            "status": "WARN",
            "alert_text": "AWS Next Gen: Game-Script Panic Threshold breached. Heavy protection collapse."
        }
    ]
}

def fire_live_update():
    print(f"📡 Connecting to data feed matrix at: {TARGET_URL}...")
    try:
        response = requests.post(TARGET_URL, json=live_payload)
        if response.status_code == 200:
            print("✅ SUCCESS: Live game data payload injected successfully!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ FAILED: Server returned status code {response.status_code}")
            print(response.text)
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Make sure your Flask application is running and accessible!")

if __name__ == "__main__":
    fire_live_update()

