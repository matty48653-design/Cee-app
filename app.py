from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    # DIRECT PRODUCTION LIVE DATA INJECTION
    slate = {
        "game": "Atlanta Falcons @ New Orleans Saints",
        "live_clock": "4TH QTR - LIVE",
        "score_string": "ATL 45 - 17 NO",
        "closing_line": 47.5,
        "sim_total": 62,
        "pacing_status": "Pacing 💥 OVER"
    }
    
    players = [
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
    ]
    
    morale = [
        {
            "unit": "Saints O-Line",
            "status": "WARN",
            "alert_text": "AWS Next Gen: Game-Script Panic Threshold breached. Heavy protection collapse."
        }
    ]
    
    return render_template("dashboard.html", slate=slate, players=players, morale=morale)

if __name__ == '__main__':
    app.run(debug=True)
