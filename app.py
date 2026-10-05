import os
import requests
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- CEE ENGINE TIGHT DATA FILTERS ---
# Explicitly isolates target slates and completely blocks unwanted feeds
ALLOWED_LEAGUES = ['NFL', 'CFB', 'NHL']
BLOCKED_BET_TYPES = ['puck_line', 'mlb_moneyline']

def fetch_and_filter_cee_matrix():
    """
    Fetches real-time sports metrics and filters out emotional public narrative biases.
    Strictly removes all legacy ticker background memory loops to save local device processing.
    """
    # Replace this placeholder with your live data streaming endpoint URL
    DATA_ENDPOINT = "https://example.com"
    
    try:
        response = requests.get(DATA_ENDPOINT, timeout=10)
        if response.status_code != 200:
            return []
        
        raw_data = response.json()
        filtered_matrix = []
        
        for item in raw_data.get("games", []):
            league = item.get("league", "").upper()
            bet_type = item.get("bet_type", "").lower()
            
            # 1. Pipeline Scope Enforcement (Blocks MLB and Puck Lines at the gate)
            if league not in ALLOWED_LEAGUES:
                continue
            if bet_type in BLOCKED_BET_TYPES:
                continue
                
            # 2. Morale Deficit Penalty Module (Injury-driven psychological decay tracking)
            injury_multiplier = item.get("morale_deficit_penalty", 1.0)
            
            # 3. Game-Script Panic Threshold Module (Line manipulation decay tracking)
            public_money = item.get("public_money_percentage", 50)
            line_movement = item.get("line_movement_direction", "neutral")
            
            # CEE Milestone Formula: Flag contrarian gaps matching passing/rushing stats
            if public_money > 75 and line_movement == "reverse":
                item["cee_edge_rating"] = "CRITICAL CONTRARIAN"
            elif injury_multiplier > 1.25:
                item["cee_edge_rating"] = "HIGH EDGE"
            else:
                item["cee_edge_rating"] = "STANDARD MATCHUP"
                
            filtered_matrix.append(item)
            
        return filtered_matrix
        
    except Exception as e:
        # Prevents mobile app layout crashes if connection times out
        return [{"error": f"Data connection idle: {str(e)}", "league": "SYS", "cee_edge_rating": "ERROR"}]

# --- JAVASCRIPT-FREE CSS INTERFACE (v5.3 Clean-Table-Matrix Layout) ---
# Hardcoded design prioritizing scannability and structural frame sizes for phone screens
MATRIX_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CEE Engine v5.3</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #121212;
            color: #E0E0E0;
            margin: 0;
            padding: 12px;
        }
        .matrix-frame {
            max-width: 600px;
            margin: 0 auto;
        }
        header {
            border-bottom: 2px solid #2C2C2C;
            padding-bottom: 8px;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        h1 { font-size: 1.1rem; color: #00E676; margin: 0; letter-spacing: 0.5px; }
        .ver-tag { font-size: 0.7rem; color: #757575; font-weight: bold; }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            background-color: #1E1E1E;
            border-radius: 6px;
            overflow: hidden;
        }
        th, td {
            padding: 12px 10px;
            text-align: left;
            border-bottom: 1px solid #2C2C2C;
        }
        th { background-color: #262626; color: #888; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; }
        .edge-badge {
            padding: 3px 6px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.65rem;
        }
        .EDGE-CRITICAL { background-color: #D32F2F; color: #FFF; }
        .EDGE-HIGH { background-color: #F57C00; color: #FFF; }
        .EDGE-STANDARD { background-color: #388E3C; color: #FFF; }
    </style>
</head>
<body>
    <div class="matrix-frame">
        <header>
            <h1>CONTRARIAN EDGE ENGINE</h1>
            <span class="ver-tag">v5.3 CLEAN-MATRIX</span>
        </header>
        
        <table>
            <thead>
                <tr>
                    <th style="width: 20%;">LEAGUE</th>
                    <th style="width: 55%;">MATCHUP ANALYSIS</th>
                    <th style="width: 25%;">CEE EDGE</th>
                </tr>
            </thead>
            <tbody>
                {% if matrix %}
                    {% for row in matrix %}
                    <tr>
                        <td><strong>{{ row.get('league', 'N/A') }}</strong></td>
                        <td>{{ row.get('description', 'No parameters discovered') }}</td>
                        <td>
                            {% set rating = row.get('cee_edge_rating', 'STANDARD MATCHUP') %}
                            {% if 'CRITICAL' in rating %}
                                <span class="edge-badge EDGE-CRITICAL">CRITICAL</span>
                            {% elif 'HIGH' in rating %}
                                <span class="edge-badge EDGE-HIGH">HIGH EDGE</span>
                            {% else %}
                                <span class="edge-badge EDGE-STANDARD">STABLE</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                {% else %}
                    <tr>
                        <td colspan="3" style="text-align:center; color:#757575; padding: 24px 0;">No active public anomalies. Workspace clear.</td>
                    </tr>
                {% endif %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

@app.route('/')
def live_matrix_dashboard():
    active_matrix = fetch_and_filter_cee_matrix()
    return render_template_string(MATRIX_UI, matrix=active_matrix)

@app.route('/api/status')
def backend_health_check():
    return jsonify({"status": "active", "build_scope": ALLOWED_LEAGUES, "version": "5.3"})

if __name__ == '__main__':
    # Dynamically maps to the active environment port managed by Render
    server_port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=server_port)
