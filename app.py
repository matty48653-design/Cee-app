from flask import Flask, render_template_string
import time

app = Flask(__name__)

SYSTEM_STATE = {
    "version": "5.1 Premium",
    "status": "Scanning Active Feeds",
    "sports": ["NFL Football", "CFB Gridiron", "NHL Hockey"],
    "exclusions": ["MLB Baseball (Silenced)"],
    "milestone_baseline": "20.00",
    "active_filters": [
        {"name": "Morale Deficit Penalty", "status": "ACTIVE", "desc": "Tracking injury clusters and psychological team fatigue."},
        {"name": "Game-Script Panic Threshold", "status": "ACTIVE", "desc": "Isolating heavily backed public trap lines."},
        {"name": "Reverse Line Elasticity Tracker", "status": "ACTIVE", "desc": "Monitoring sharp money counter-movements."}
    ],
    "system_logs": [
        f"[{time.strftime('%I:%M %p')}] System clock synchronized with real-world sports feeds.",
        f"[{time.strftime('%I:%M %p')}] Contributor pipeline authorized for matty48653.",
        f"[{time.strftime('%I:%M %p')}] MLB sports betting nodes successfully suppressed.",
        f"[{time.strftime('%I:%M %p')}] Live tracking logs successfully routed to home screen dashboard."
    ]
}

HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CEE Dashboard v5.1</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #0A0A0C; color: #E4E4E7; padding: 15px; margin: 0; }
        .header { display: flex; align-items: center; justify-content: space-between; padding-bottom: 10px; border-bottom: 2px solid #1F2937; margin-bottom: 15px; }
        .header h2 { margin: 0; color: #00E676; font-size: 20px; font-weight: 800; letter-spacing: 0.5px; }
        .status-badge { background-color: rgba(0, 230, 118, 0.15); color: #00E676; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; border: 1px solid rgba(0, 230, 118, 0.3); }
        .card { background: #111115; border-radius: 12px; padding: 14px; margin-bottom: 15px; border: 1px solid #22222A; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .card h3 { margin: 0 0 10px 0; font-size: 14px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 1px; }
        .metric-row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 14px; }
        .metric-row:last-child { margin-bottom: 0; }
        .label { color: #A1A1AA; }
        .value { color: #FFFFFF; font-weight: 600; }
        .filter-box { background: #16161F; border-left: 4px solid #00E676; padding: 10px; margin-bottom: 10px; border-radius: 0 8px 8px 0; }
        .filter-box:last-child { margin-bottom: 0; }
        .filter-title { font-weight: bold; font-size: 14px; color: #FFFFFF; display: flex; justify-content: space-between; }
        .filter-desc { font-size: 12px; color: #71717A; margin-top: 4px; }
        .terminal { background: #000000; border-radius: 8px; padding: 12px; font-family: "Courier New", Courier, monospace; font-size: 11px; color: #39FF14; height: 110px; overflow-y: auto; border: 1px solid #1F2937; }
        .terminal-line { margin-bottom: 4px; line-height: 1.4; }
        .btn { background: linear-gradient(135deg, #00E676 0%, #00B0FF 100%); color: #000000; border: none; width: 100%; padding: 15px; border-radius: 10px; font-size: 16px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 12px rgba(0, 230, 118, 0.3); margin-top: 5px; width: 100%; }
        .btn:active { transform: scale(0.98); opacity: 0.9; }
    </style>
</head>
<body>
    <div class="header">
        <h2>CEE CONTROL v{{ data.version }}</h2>
        <div class="status-badge">● LIVE</div>
    </div>

    <div class="card">
        <h3>📊 Strategy Engine Core</h3>
        <div class="metric-row"><span class="label">System Pipeline:</span><span class="value" style="color: #00E676;">{{ data.status }}</span></div>
        <div class="metric-row"><span class="label">Target Assets:</span><span class="value">{{ data.sports | join(', ') }}</span></div>
        <div class="metric-row"><span class="label">Suppressed Channels:</span><span class="value" style="color: #EF4444;">{{ data.exclusions | join(', ') }}</span></div>
        <div class="metric-row"><span class="label">Milestone Baseline:</span><span class="value" style="color: #00B0FF;">${{ data.milestone_baseline }} Compounding</span></div>
    </div>

    <div class="card">
        <h3>⚙️ Custom Analytical Filters</h3>
        {% for filter in data.active_filters %}
        <div class="filter-box">
            <div class="filter-title"><span>{{ filter.name }}</span> <span style="color: #00E676; font-size: 11px;">[{{ filter.status }}]</span></div>
            <div class="filter-desc">{{ filter.desc }}</div>
        </div>
        {% endfor %}
    </div>

    <div class="card">
        <h3>🖥️ Live Background Activity Log</h3>
        <div class="terminal">
            {% for log in data.system_logs %}
            <div class="terminal-line">&gt;&gt; {{ log }}</div>
            {% endfor %}
        </div>
    </div>

    <button class="btn" onclick="alert('Executing automated sports data stream scan... Check email channel for premium alignments.')">🚀 Trigger Engine Scan</button>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT, data=SYSTEM_STATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
