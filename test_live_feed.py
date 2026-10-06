import time
import requests

# Production URL preset for direct deployment
TARGET_URL = "https://onrender.com"

yesterday_simulation_slate = [
    # STATE 1: LIONS SLATE OPENER
    {
        "slate": {
            "game": "Detroit Lions @ Carolina Panthers",
            "live_clock": "1ST QTR - 08:45",
            "score_string": "DET 7 - 3 CAR",
            "closing_line": 46.5,
            "sim_total": 49,
            "pacing_status": "Pacing 🔥 STABLE"
        },
        "players": [
            {"name": "Jared Goff", "position": "QB", "target": "Over 238.5 Pass Yards Floor (45 YDS)", "is_floor": True},
            {"name": "Amon-Ra St. Brown", "position": "WR", "target": "Under 6.5 Receptions Ceiling (1 REC)", "is_floor": False}
        ],
        "morale": [
            {"unit": "Panthers Run Def", "status": "WARN", "alert_text": "CEE Floor Gauge: Public heavily backing DET. Track line adjustments."}
        ]
    },
    # STATE 2: LIONS VS PANTHERS LATE TRAP CLOSURE
    {
        "slate": {
            "game": "Detroit Lions @ Carolina Panthers",
            "live_clock": "4TH QTR - FINAL",
            "score_string": "DET 26 - 32 CAR",
            "closing_line": 46.5,
            "sim_total": 58,
            "pacing_status": "Pacing 💥 OVER"
        },
        "players": [
            {"name": "Jared Goff", "position": "QB", "target": "Over 238.5 Pass Yards Floor (244 YDS - CLEARED)", "is_floor": True},
            {"name": "Amon-Ra St. Brown", "position": "WR", "target": "Under 6.5 Receptions Ceiling (7 REC - BREACHED)", "is_floor": False}
        ],
        "morale": [
            {"unit": "Lions Secondary", "status": "WARN", "alert_text": "Game-Script Panic Threshold breached. High public backing collapsed late."}
        ]
    },
    # STATE 3: COWBOYS @ TEXANS IN-GAME PRESSURE LIVE MODEL
    {
        "slate": {
            "game": "Dallas Cowboys @ Houston Texans",
            "live_clock": "3RD QTR - 02:15",
            "score_string": "DAL 24 - 20 HOU",
            "closing_line": 51.5,
            "sim_total": 56,
            "pacing_status": "Pacing 🔥 OVER"
        },
        "players": [
            {"name": "Dak Prescott", "position": "QB", "target": "Over 265.5 Pass Yards Floor (198 YDS)", "is_floor": True},
            {"name": "CeeDee Lamb", "position": "WR", "target": "Under 7.5 Receptions Ceiling (5 REC)", "is_floor": False}
        ],
        "morale": [
            {"unit": "Texans O-Line", "status": "WARN", "alert_text": "AWS Pressure Metric: High pocket collapse trajectory active."}
        ]
    },
    # STATE 4: COWBOYS @ TEXANS TRAP OUTCOME REVELATION
    {
        "slate": {
            "game": "Dallas Cowboys @ Houston Texans",
            "live_clock": "4TH QTR - FINAL",
            "score_string": "DAL 34 - 30 HOU",
            "closing_line": 51.5,
            "sim_total": 64,
            "pacing_status": "Pacing 💥 OVER"
        },
        "players": [
            {"name": "Dak Prescott", "position": "QB", "target": "Over 265.5 Pass Yards Floor (282 YDS - CLEARED)", "is_floor": True},
            {"name": "CeeDee Lamb", "position": "WR", "target": "Under 7.5 Receptions Ceiling (6 REC - SAFE)", "is_floor": False}
        ],
        "morale": [
            {"unit": "Texans Secondary", "status": "WARN", "alert_text": "Increment Gain Strategy: Money line shifted late to public trap exit."}
        ]
    },
    # STATE 5: CHIEFS @ RAIDERS TIED DIVISION SLUGFEST
    {
        "slate": {
            "game": "Kansas City Chiefs @ Las Vegas Raiders",
            "live_clock": "4TH QTR - FINAL",
            "score_string": "KC 30 - 27 LV",
            "closing_line": 44.5,
            "sim_total": 57,
            "pacing_status": "Pacing 💥 OVER"
        },
        "players": [
            {"name": "Patrick Mahomes", "position": "QB", "target": "Over 235.5 Pass Yards Floor (242 YDS - CLEARED)", "is_floor": True},
            {"name": "Travis Kelce", "position": "TE", "target": "Under 5.5 Receptions Ceiling (4 REC - SAFE)", "is_floor": False}
        ],
        "morale": [
            {"unit": "Raiders Front 7", "status": "WARN", "alert_text": "Morale DeficitStream: Final drive fatigue penalty logged."}
        ]
    },
    # STATE 6: RAMS @ EAGLES PUBLIC MONEY FADE OUTCOME
    {
        "slate": {
            "game": "Los Angeles Rams @ Philadelphia Eagles",
            "live_clock": "4TH QTR - FINAL",
            "score_string": "LAR 24 - 20 PHI",
            "closing_line": 48.5,
            "sim_total": 44,
            "pacing_status": "Pacing 📉 UNDER"
        },
        "players": [
            {"name": "Matthew Stafford", "position": "QB", "target": "Over 224.5 Pass Yards Floor (231 YDS - CLEARED)", "is_floor": True},
            {"name": "Kyren Williams", "position": "RB", "target": "Under 88.5 Rush Yards Ceiling (72 YDS - SAFE)", "is_floor": False}
        ],
        "morale": [
            {"unit": "Eagles Secondary", "status": "WARN", "alert_text": "Public Trap Faded: 82% public money line on favored home team fails."}
        ]
    }
]

def run_historical_loop():
    print(f"📡 CONTRARIAN SLATE SIMULATOR RUNNING -> CONNECTED TO PRODUCTION AT: {TARGET_URL}")
    print("Press Ctrl+C inside this console tab to terminate the simulation.\n")
    
    state_index = 0
    while True:
        payload = yesterday_simulation_slate[state_index]
        print(f"⚡ Streaming [State {state_index + 1}/6]: {payload['slate']['game']} ({payload['slate']['live_clock']})")
        
        try:
            response = requests.post(TARGET_URL, json=payload)
            if response.status_code == 200:
                print("   👉 Payload injected successfully into live Render server Matrix.")
            else:
                print(f"   ❌ FAILED to update production. Status code: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("   ❌ PRODUCTION TIMEOUT: Link broken or Render web instance sleeping.")
            break
            
        state_index = (state_index + 1) % len(yesterday_simulation_slate)
        time.sleep(4) # Rotates the matchup profile on your screen every 4 seconds

if __name__ == "__main__":
    run_historical_loop()
