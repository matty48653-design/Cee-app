from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Active Contrarian Edge Engine configuration filters
ALLOWED_SPORTS = ['NFL', 'CFB', 'NHL']
BLOCKED_MARKETS = ['puck_line', 'mlb']

def get_contrarian_matrix():
    """
    Tracks and filters sports matchups based on money flow.
    Limits data processing strictly to milestone thresholds, money lines, 
    and over/unders for allowed sports.
    """
    # Raw sports feed endpoint placeholder
    raw_feed = [] 
    
    clean_matrix = []
    for market_data in raw_feed:
        sport = market_data.get('sport')
        market_type = market_data.get('market_type')
        
        # Strict validation checks
        if sport in ALLOWED_SPORTS and market_type not in BLOCKED_MARKETS:
            clean_matrix.append({
                'sport': sport,
                'matchup': market_data.get('matchup'),
                'line': market_data.get('line'),
                'public_percentage': market_data.get('public_percentage'),
                'money_flow': market_data.get('money_flow')
            })
            
    return clean_matrix

@app.route('/')
def index():
    # Primary dashboard visual interface layout (Dark Mode Matrix)
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CEE v5.3 Matrix</title>
        <style>
            body { font-family: -apple-system, sans-serif; background-color: #121212; color: #ffffff; padding: 16px; margin: 0; }
            h1 { color: #00e676; font-size: 22px; margin-bottom: 4px; font-weight: 700; }
            p { color: #888888; font-size: 14px; margin-top: 0; margin-bottom: 24px; }
            .matrix-table { width: 100%; border-collapse: collapse; margin-top: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
            .matrix-table th, .matrix-table td { padding: 14px; border: 1px solid #2c2c2c; text-align: left; font-size: 14px; }
            .matrix-table th { background-color: #1e1e1e; color: #00e676; font-weight: 600; text-transform: uppercase; font-size: 12px; letter-spacing: 0.5px; }
            .matrix-table tr:nth-child(even) { background-color: #1a1a1a; }
            .tag { background: #2979ff; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; letter-spacing: 0.5px; }
            .tag.nfl { background: #1565c0; }
            .tag.nhl { background: #37474f; }
        </style>
    </head>
    <body>
        <h1>Contrarian Edge Engine</h1>
        <p>v5.3 • Clean Table Matrix Active</p>
        <table class="matrix-table">
            <thead>
                <tr>
                    <th>Sport</th>
                    <th>Matchup</th>
                    <th>Target Milestones / Line</th>
                    <th>Public %</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><span class="tag nfl">NFL</span></td>
                    <td>Detroit Lions Matchup Active</td>
                    <td>Passing / Rushing Milestones Active</td>
                    <td>Scanning...</td>
                </tr>
                <tr>
                    <td><span class="tag nhl">NHL</span></td>
                    <td>Tonight's Matchup</td>
                    <td>Money Line / Totals Only (Puck Line Blocked)</td>
                    <td>Scanning...</td>
                </tr>
            </tbody>
        </table>
    </body>
    </html>
    """

@app.route('/api/matrix')
def matrix_api():
    # Direct backend API for data verification
    data = get_contrarian_matrix()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
