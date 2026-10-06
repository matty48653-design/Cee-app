import time
import requests

# Set production link: "https://onrender.com"
TARGET_URL = "http://127.0.0"

lions_game_payload = {
    "slate": {
        "game": "Detroit Lions @ Green Bay Packers",
        "live_clock": "2ND QTR - 04:12",
        "score_string": "DET 24 - 10 GB",
        "closing_line": 49.5,
        "sim_total": 58,
        "pacing_status": "Pacing 💥 OVER"
    },
    "players": [
        {
            "name": "Jared Goff",
            "position": "QB",
            "target": "Over 242.5 Passing Yards Floor (165 YDS - ACTIVE)",
            "is_floor": True
        },
        {
            "name": "Amon-Ra St. Brown",
            "position": "WR",
            "target": "Under 6.5 Live Receptions Ceiling (2 REC - ACTIVE)",
            "is_floor": False
        }
    ],
    "morale": [
        {
            "unit": "Packers Secondary",
            "status": "WARN",
            "alert_text": "Morale Deficit Penalty engaged. Game-Script Panic Threshold breached."
        }
    ]
}

def inject_lions_slate():
    print(f"📡 Forwarding Lions Contrarian Matrix Payload to {TARGET_URL}...")
    try:
        response = requests.post(TARGET_URL, json=lions_game_payload)
        if response.status_code == 200:
            print("✅ SUCCESS: Lions Game State updated live on the UI!")
        else:
            print(f"❌ FAILED: Code {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ SERVER DOWN: Fire up app.py before executing the feed data injection.")

if __name__ == "__main__":
    inject_lions_slate()
