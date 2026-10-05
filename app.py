from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Active Contrarian Edge Engine configuration filters
ALLOWED_SPORTS = ['NFL', 'CFB', 'NHL']
BLOCKED_MARKETS = ['puck_line', 'mlb']

def get_contrarian_matrix():
    """
    Fetches live betting lines and structures the contrarian data matrix.
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
            # Drops legacy scrolling ticker memory loops
            # Formats data cleanly for a single table view on your Galaxy smartphone
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
    # Primary dashboard layout route
    return "<h1>CEE v5.3 - Clean Table Matrix Active</h1>"

@app.route('/api/matrix')
def matrix_api():
    # Direct backend API for the clean data grid
    data = get_contrarian_matrix()
    return jsonify(data)

if __name__ == '__main__':
    # Binds to all interfaces for cloud container mapping
    app.run(host='0.0.0.0', port=5000)
