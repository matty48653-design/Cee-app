<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CEE v5.3 HUD</title>
    <style>
        body { background-color: #0d0f14; color: #cbd5e1; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 16px; }
        .banner { background: #1e1b4b; border: 1px solid #3b82f6; color: #38bdf8; text-align: center; padding: 10px; font-weight: bold; border-radius: 6px; font-size: 12px; letter-spacing: 0.05em; margin-bottom: 20px; }
        .section-title { font-size: 14px; font-weight: 700; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.1em; margin: 24px 0 12px 0; border-left: 3px solid #ef4444; padding-left: 8px; }
        .matrix-table { width: 100%; border-collapse: collapse; background: #111827; border-radius: 8px; overflow: hidden; border: 1px solid #1f2937; margin-bottom: 20px; }
        .matrix-table th { background: #1f2937; color: #94a3b8; font-size: 11px; text-transform: uppercase; text-align: left; padding: 12px; font-weight: 600; }
        .matrix-table td { padding: 14px 12px; font-size: 13px; border-bottom: 1px solid #1f2937; }
        .matrix-table tr:last-child td { border-bottom: none; }
        .badge { background: #1e3a8a; color: #60a5fa; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 600; display: inline-block; }
        .badge-alt { background: #7c2d12; color: #f97316; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 600; display: inline-block; }
    </style>
</head>
<body>

    <div class="banner">⚡ ENGINE STATUS: REAL-TIME LIVE DATA CHANNELS ACTIVE</div>

    <div class="section-title">Live Dynamic Tracker Slates</div>
    <table class="matrix-table">
        <thead>
            <tr>
                <th>League</th>
                <th>Matchup</th>
                <th>Live Score</th>
                <th>Game Status</th>
                <th>CEE Target Metric</th>
            </tr>
        </thead>
        <tbody>
            {% if cache.slates %}
                {% for game in cache.slates %}
                <tr>
                    <td><span class="badge">{{ game.league }}</span></td>
                    <td><b>{{ game.matchup }}</b></td>
                    <td style="color: #4ade80; font-weight: bold; font-family: monospace;">{{ game.score }}</td>
                    <td><small style="color: #94a3b8;">{{ game.line_value }}</small></td>
                    <td><span class="badge-alt">{{ game.target_value }}</span></td>
                </tr>
                {% endfor %}
            {% else %}
                <tr>
                    <td colspan="5" style="text-align: center; color: #94a3b8; padding: 20px;">
                        Initializing Background Connection Stream... Refresh in a moment.
                    </td>
                </tr>
            {% endif %}
        </tbody>
    </table>

</body>
</html>
