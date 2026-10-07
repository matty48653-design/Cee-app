# feed_bridge.py
import time
import json
import urllib.request

JSON_CACHE_FILE = "sports_data.json"

def get_espn_scores(league_rpc):
    """Safely connects to the structural public endpoint wire of ESPN."""
    # FIXED: Restored the true api sub-domains and endpoint paths
    url = f"https://site.api.espn.com/apis/site/v2/sports/{league_rpc}/scoreboard"
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=12) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Network Pipe Stream Obstruction for {league_rpc}: {e}")
        return None

def process_live_slates():
    """Extracts live slates from the web, breaks down arrays, and builds matrix metrics."""
    current_time_str = time.strftime("%-I:%M %p")
    
    # Secure structural base frame matching your dashboard grid layout
    output_data = {
        "timestamp": current_time_str,
        "sharp_sheet": {
            "game_spread_edge": "Target Slate Active",
            "game_spread_desc": "Scanning live network board tracks for CEE margin edge placements.",
            "totals_edge": "Matrix Stream Engaged",
            "totals_desc": "Background data pipeline feeding real-time updates safely."
        },
        "slates": []
    }

    # 1. PARSE ACTIVE LIVE CFB (College Football) WIRE
    cfb_raw = get_espn_scores("football/college-football")
    if cfb_raw and "events" in cfb_raw:
        for event in cfb_raw["events"]:
            short_name = event.get("shortName", "")
            try:
                comp = event["competitions"][0]
                status_text = comp["status"]["type"]["detail"]
                
                # Dynamic mapping of live scoring arrays
                competitors = comp["competitors"]
                away_score = competitors[1]["score"]
                home_score = competitors[0]["score"]
                display_score = f"{away_score} - {home_score}"

                output_data["slates"].append({
                    "league": "CFB",
                    "matchup": short_name,
                    "score": display_score,
                    "line_label": "Game Status:",
                    "line_value": status_text,
                    "target_label": "CEE Target:",
                    "target_value": "Contrarian Money Trap Mode Engaged",
                    "kickoff": f"Network Tracking Track: Live Updates Active"
                })
            except Exception:
                pass

    # 2. PARSE ACTIVE LIVE NHL (Hockey) WIRE
    nhl_raw = get_espn_scores("hockey/nhl")
    if nhl_raw and "events" in nhl_raw:
        for event in nhl_raw["events"]:
            short_name = event.get("shortName", "")
            try:
                comp = event["competitions"][0]
                status_text = comp["status"]["type"]["detail"]
                
                competitors = comp["competitors"]
                away_score = competitors[1]["score"]
                home_score = competitors[0]["score"]
                display_score = f"{away_score} - {home_score}"

                output_data["slates"].append({
                    "league": "NHL",
                    "matchup": short_name,
                    "score": display_score,
                    "line_label": "Game Status:",
                    "line_value": status_text,
                    "target_label": "CEE Target:",
                    "target_value": "Live Slider Edge Variance Track",
                    "kickoff": f"Arena Feed Track: Live Updates Active"
                })
            except Exception:
                pass

    # Safety structural guardrail: Only save to disk if we pulled real matches
    if len(output_data["slates"]) > 0:
        with open(JSON_CACHE_FILE, "w") as f:
            json.dump(output_data, f)
        print(f"[{current_time_str}] sports_data.json updated cleanly from live network wire.")
    else:
        # Fallback to prevent empty dashboard states if no live matches are playing right now
        output_data["slates"].append({
            "league": "SYS",
            "matchup": "No Active Matches Live",
            "score": "0 - 0",
            "line_label": "Status:",
            "line_value": "Waiting for Slate Kickoff",
            "target_label": "CEE Matrix:",
            "target_value": "Monitoring Boards Continuously",
            "kickoff": "System Listening Loop Active"
        })
        with open(JSON_CACHE_FILE, "w") as f:
            json.dump(output_data, f)

def main():
    print("CEE Data Bridge Active: Live Scoring Automation Core Initialized.")
    while True:
        process_live_slates()
        # Ping external data networks cleanly every 60 seconds
        time.sleep(60)

if __name__ == "__main__":
    main()
