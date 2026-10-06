from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Hardcoded sample engine data strictly matching the HUD's expected keys
    tracking_data = [
        {
            "teams": "Lions vs Bears",
            "league": "NFL",
            "edge": "+3.5 Edge",
            "milestone": "Passing Alt Line"
        },
        {
            "teams": "Red Wings vs Lightning",
            "league": "NHL",
            "edge": "Under 6.5",
            "milestone": "Alt Total Matchup"
        }
    ]
    return render_template('dashboard.html', tracking_items=tracking_data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
