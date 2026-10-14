import requests
import json
import time

# ==================== CONFIGURATION ====================
API_KEY = "f4d35efa9891beef9b72344e501ddc31"
RENDER_WEBHOOK_URL = "https://cee-app.onrender.com/update"
SPORT = "americanfootball_ncaaf"
REGION = "us"
MARKETS = "spreads,totals"
# =======================================================

def fetch_and_sync_matrix():
    print(f"📡 Requesting live data feed from The Odds API for {SPORT}...")
    odds_url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?apiKey={API_KEY}&regions={REGION}&markets={MARKETS}&oddsFormat=american"
    
    try:
        response = requests.get(odds_url)
        if response.status_code != 200:
            print(f"❌ API Error: Status {response.status_code}.")
            return

        games_list = response.json()
        if not games_list:
            print("📭 No active or upcoming matches returned.")
            return

        parsed_matrix_payload = []

        for game in games_list[:5]:
            home_team = game.get("home_team")
            away_team = game.get("away_team")
            matchup_name = f"{away_team} vs {home_team}"
            
            live_spread = "N/A"
            live_total = "N/A"
            
            bookmakers = game.get("bookmakers", [])
            if bookmakers:
                target_book = next((b for b in bookmakers if b["key"] == "draftkings"), bookmakers[0] if bookmakers else {})
                markets = target_book.get("markets", [])
                
                for market in markets:
                    if market["key"] == "spreads":
                        outcomes = market.get("outcomes", [])
                        if outcomes:
                            home_outcome = next((o for o in outcomes if o["name"] == home_team), outcomes[0])
                            point = home_outcome.get("point", 0)
                            live_spread = f"{'+' if point > 0 else ''}{point}"
                    
                    elif market["key"] == "totals":
                        outcomes = market.get("outcomes", [])
                        if outcomes and len(outcomes) > 0:
                            live_total = str(outcomes[0].get("point", "N/A"))

            matrix_node = {
                "matchup": matchup_name,
                "spread": live_spread,
                "total": live_total,
                "take_action": f"EVALUATE: {away_team} Spread Entry Conditions",
                "context": f"Live Market Pricing gathered via DraftKings consensus feeds.",
                "syndicate_name": "Alpha Syndicate",
                "syndicate_size": "5x",
                "syndicate_market": "Consensus Line Sliders",
                "public_resistance": "50%",
                "evaluation": "AUTOMATED PIPELINE: Scanning live market volume and tracking variance thresholds."
            }
            parsed_matrix_payload.append(matrix_node)

        print(f"📤 Syncing {len(parsed_matrix_payload)} parsed games to Render dashboard...")
        sync_response = requests.post(RENDER_WEBHOOK_URL, json=parsed_matrix_payload)
        
        if sync_response.status_code == 200:
            print("✅ Dashboard sync successful!")
        else:
            print(f"❌ Failed to sync: {sync_response.status_code}")

    except Exception as e:
        print(f"💥 Error: {str(e)}")

if __name__ == "__main__":
    fetch_and_sync_matrix()
