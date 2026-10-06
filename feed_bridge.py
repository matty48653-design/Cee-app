import time
import requests

# 🟢 TARGET PRODUCTION URL FOR RENDER
TARGET_URL = "https://onrender.com"

def capture_and_bridge():
    print(f"🚀 HOME FEED BRIDGE ONLINE -> DEPLOYING TO: {TARGET_URL}")
    print("Keep this terminal script open during the games to push live stats!\n")
    
    while True:
        # 1. Fetch unblocked data from ESPN's raw public feeds locally
        nhl_url = "https://espn.com"
        nfl_url = "https://espn.com"
        
        slates_payload = []
        
        try:
            # PROCESS LIVE HOCKEY GAMES
            nhl_res = requests.get(nhl_url, timeout=5).json()
            for event in nhl_res.get("events", []):
                name = event.get("name", "NHL Matchup").replace(" at ", " @ ")
                # Structural filter to isolate games matching your locked DraftKings slips
                if "Islanders" in name or "Red Wings" in name or "Panthers" in name:
                    detail = event.get("status", {}).get("type", {}).get("detail", "PRE-GAME")
                    
                    # Extracting score totals smoothly
                    scores = ["0", "0"]
                    competitors = event.get("competitions", [{}])[0].get("competitors", [])
                    if len(competitors) >= 2:
                        scores = [competitors[1].get("score", "0"), competitors[0].get("score", "0")]
                    score_str = f"{scores[0]} - {scores[1]}"
                    
                    slates_payload.append({
                        "sport_tag": "专 ACTIVE HOCKEY SLATE",
                        "game": name,
                        "live_clock": detail.upper(),
                        "score_string": score_str,
                        "closing_line": "O/U 5.5" if "Red Wings" not in name else "O/U 6.5",
                        "sim_total": "Live Tracker Synchronized",
                        "pacing_status": "LIVE UPDATING",
                        "players": [{"name": "Tracking Live Stats", "position": "CEE", "target": "Active Slip Channel Open", "is_floor": True}],
                        "morale": [{"unit": "Live Feed", "status": "OK", "alert_text": "Data packet forwarded via secure home gate link."}]
                    })
                    
            # PROCESS NFL SLATES
            nfl_res = requests.get(nfl_url, timeout=5).json()
            for event in nfl_res.get("events", []):
                name = event.get("name", "NFL Matchup").replace(" at ", " @ ")
                if "Lions" in name:
                    detail = event.get("status", {}).get("type", {}).get("detail", "PRE-GAME")
                    slates_payload.append({
                        "sport_tag": "🏈 CONTRARIAN FOOTBALL SLATE",
                        "game": name,
                        "live_clock": detail.upper(),
                        "score_string": "PRE-GAME",
                        "closing_line": "O/U 52.5",
                        "sim_total": "CEE Projected: 57",
                        "pacing_status": "Pacing Initialized",
                        "players": [{"name": "Jared Goff", "position": "QB", "target": "Over 248.5 Passing Yards Floor", "is_floor": True}],
                        "morale": [{"unit": "Cardinals Sec", "status": "WARN", "alert_text": "Tracking public money fade ratios on kickoff."}]
                    })
                    
            # 2. Fire the packed data right through Render's gate
            if slates_payload:
                response = requests.post(TARGET_URL, json={"slates": slates_payload}, timeout=5)
                if response.status_code == 200:
                    print(f"✅ Injected data packet successfully at {time.strftime('%H:%M:%S')}")
                else:
                    print(f"❌ Gate rejected packet: Status {response.status_code}")
                    
        except Exception as e:
            print(f"⚠️ Transmission error loop: {e}")
            
        time.sleep(15) # Refresh the stats smoothly every 15 seconds

if __name__ == "__main__":
    capture_and_bridge()

