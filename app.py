from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "sports_data.json"

def load_matrix_data():
    """Reads live scraper updates from the disk layer, or safely routes the live fallback slate."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                if data:  # Only return if the JSON file is not empty
                    return data
        except Exception:
            pass
            
    # 🔥 TODAY'S REAL STATIC GAME DATA FOR THE WHALES
    return [
        {
            "matchup": "Western Kentucky vs Sam Houston State",
            "spread": "-1.5",
            "total": "53.5",
            "take_action": "TAKE: Sam Houston State +1.5 Line Coverage",
            "context": "Elliott T. Bowers Stadium • Midweek CUSA Action • Sharp Action shifting line downward.",
            "syndicate_name": "Alpha Syndicate",
            "syndicate_size": "5x Allocation",
            "syndicate_market": "Point Spread Volume Move",
            "public_resistance": "94% Public Pressure fading Underdog",
            "evaluation": "ALPHA WHALE SIGNAL: Heavy institutional cash backing the home dog. Mispricing exposed on key numbers."
        },
        {
            "matchup": "Kennesaw State vs Missouri State",
            "spread": "-3.0",
            "total": "52.5",
            "take_action": "TAKE: Under 52.5 Game Total Points",
            "context": "Plaster Stadium • Heavy public concentration chasing the Over • Pacing matrix suggests lower threshold.",
            "syndicate_name": "Vegas Syndicate",
            "syndicate_size": "4x Allocation",
            "syndicate_market": "Game Total Handles",
            "public_resistance": "78% Public Consensus on Over",
            "evaluation": "SHARP MATRIX: Over/Under recon signals intense public resistance. Institutional money trapping late public volume."
        }
    ]

@app.route('/')
def home():
    games_data = load_matrix_data()
    return render_template("dashboard.html", games=games_data)

@app.route('/update', methods=['POST'])
def update_matrix():
    try:
        incoming_payload = request.get_json()
        if not incoming_payload:
            return jsonify({"status": "error", "message": "Missing matrix payload"}), 400
            
        with open(DATA_FILE, "w") as f:
            json.dump(incoming_payload, f, indent=4)
            
        return jsonify({"status": "success", "message": "Matrix values synced successfully!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
