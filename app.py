import os
import json
from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)

JSON_CACHE_FILE = os.path.join(os.path.dirname(__file__), "sports_data.json")

def load_live_feed_cache():
    """Reads data parameters from sports_data.json."""
    if os.path.exists(JSON_CACHE_FILE):
        try:
            with open(JSON_CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"slates": []}

@app.route("/")
def index():
    cache_data = load_live_feed_cache()
    return render_template("dashboard.html", cache=cache_data)

@app.route("/api/v5/update", methods=["POST"])
def update_matrix_data():
    """Receives manual entry inputs securely and overwrites the text data file."""
    league = request.form.get("league", "NHL")
    matchup = request.form.get("matchup", "Matchup")
    score = request.form.get("score", "O/U 6.0")
    line_value = request.form.get("line_value", "Tkts: 50%")
    target_value = request.form.get("target_value", "Sharp: 50%")
    
    current_data = load_live_feed_cache()
    
    # Append the manual entry directly into your loop array
    current_data["slates"].append({
        "league": league.upper(),
        "matchup": matchup,
        "score": score,
        "line_value": line_value,
        "target_value": target_value
    })
    
    with open(JSON_CACHE_FILE, "w") as f:
        json.dump(current_data, f)
        
    return redirect(url_for("index"))

@app.route("/api/v5/clear", methods=["POST"])
def clear_matrix_data():
    """Wipes the data clean instantly with a single button click."""
    with open(JSON_CACHE_FILE, "w") as f:
        json.dump({"slates": []}, f)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
