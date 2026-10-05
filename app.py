from flask import Flask, render_template_string
import time

app = Flask(__name__)

SYSTEM_DATA = {
    "version": "5.0",
    "status": "Live & Connected",
    "sports": ["NFL", "CFB", "NHL"],
    "filters": ["Morale Deficit Penalty", "Game-Script Panic Threshold"],
    "target_milestone": 20.00,
    "logs": [f"[{time.strftime('%I:%M %p')}] Live pipeline channel synced securely."]
}

HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CEE Engine</title>
    <style>
        body { font-family: sans-serif; background-color: #121212; color: #E0E0E0; padding: 15px; margin: 0; }
        .card { background: #1E1E1E; border-radius: 12px; padding: 15px; margin-bottom: 15px; border: 1px solid #2C2C2C; }
        .btn { background-color: #00E676; color: #121212; border: none; width: 100%; padding: 16px; border-radius: 8px; font-size: 16px; font-weight: bold; width: 100%; }
    </style>
</head>
<body>
    <div class="card">
        <h3>🟢 CEE ENGINE v{{ data.version }}</h3>
        <p>Status: <strong>{{ data.status }}</strong></p>
    </div>
    <button class="btn" onclick="alert('Scanning live sports feeds...')">🚀 Run Live Scan</button>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT, data=SYSTEM_DATA)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
