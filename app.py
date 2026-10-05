from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Active sports filtering configuration
ALLOWED_SPORTS = ['NFL', 'CFB', 'NHL']
BLOCKED_MARKETS = ['puck_line', 'mlb']

def get_contrarian_data():
    """
    Fetches and filters sports data pipeline.
    Ensures backend updates scale automatically (e.g., future NBA lines)
    without breaking the frontend presentation layer.
    """
    # Placeholder for the data feed integration
    raw_feed = [] 
    
    filtered_matrix = []
    for game in raw_feed:
        # Strict inclusion and exclusion filters
        if game.get('sport') in ALLOWED_SPORTS and game.get('market') not in BLOCKED_MARKETS:
            # Drop legacy ticker loops; structure purely for the clean matrix layout
            filtered_matrix.append(game)
            
    return filtered_matrix

@app.route('/')
def index():
    return "<h1>CEE v5.3 - Clean Table Matrix Active</h1>"

@app.route('/api/data')
def data_api():
    data = get_contrarian_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
