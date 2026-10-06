import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# THE UNIFIED CEE MASTER MATRIX - ALL SLATES RUNNING THE CONTRARIAN EDGE FILTERS
MASTER_BOARD_PORTFOLIO = [
    # ==========================================
    # 🏒 TONIGHT'S NHL MARQUEE TRACKING BOARDS (OCTOBER 6)
    # ==========================================
    {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE",
        "game": "Ottawa Senators @ Detroit Red Wings",
        "live_clock": "TONIGHT - 7:00 PM ET",
        "score_string": "0 - 0",
        "closing_line": "O/U 6.5",
        "sim_total": "Sim Total: 5.5",
        "pacing_status": "Pacing 📉 UNDER",
        "players": [
            {"name": "Dylan Larkin", "position": "C", "target": "Over 3.5 Shots on Goal Floor", "is_floor": True},
            {"name": "Tim Stützle", "position": "C", "target": "Under 2.5 Shots on Goal Ceiling", "is_floor": False}
        ],
        "morale": [{"unit": "Sens Front 6 Pacing", "status": "WARN", "alert_text": "Morale Deficit Penalty: Early season physical fatigue flagged on transition defense."}]
    },
    {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE",
        "game": "New York Islanders @ New York Rangers",
        "live_clock": "TONIGHT - 7:30 PM ET",
        "score_string": "0 - 0",
        "closing_line": "O/U 5.5",
        "sim_total": "Sim Total: 6.0",
        "pacing_status": "Pacing 🔥 EVALUATING",
        "players": [
            {"name": "Artemi Panarin", "position": "LW", "target": "Over 2.5 Shots on Goal Floor", "is_floor": True},
            {"name": "Bo Horvat", "position": "C", "target": "Under 3.5 Shots on Goal Ceiling", "is_floor": False}
        ],
        "morale": [{"unit": "Islanders Blue Line", "status": "WARN", "alert_text": "AWS Depth Metric: High expected defensive zone pressure. Ranger SOG floor highly insulated."}]
    },
    {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE",
        "game": "Carolina Hurricanes @ Montreal Canadiens",
        "live_clock": "TONIGHT - 7:00 PM ET",
        "score_string": "0 - 0",
        "closing_line": "O/U 6.0",
        "sim_total": "Sim Total: 5.5",
        "pacing_status": "Pacing 📉 UNDER",
        "players": [
            {"name": "Sebastian Aho", "position": "C", "target": "Over 2.5 Shots on Goal Floor", "is_floor": True},
            {"name": "Nick Suzuki", "position": "C", "target": "Under 2.5 Shots on Goal Ceiling", "is_floor": False}
        ],
        "morale": [{"unit": "Canadiens Goalies", "status": "WARN", "alert_text": "Public Trap Filter: 78% public consensus backing over-inflated total profile."}]
    },
    {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE",
        "game": "Nashville Predators @ Toronto Maple Leafs",
        "live_clock": "TONIGHT - 7:00 PM ET",
        "score_string": "0 - 0",
        "closing_line": "O/U 6.5",
        "sim_total": "Sim Total: 7.0",
        "pacing_status": "Pacing 💥 OVER",
        "players": [
            {"name": "Auston Matthews", "position": "C", "target": "Over 4.5 Shots on Goal Floor", "is_floor": True},
            {"name": "Filip Forsberg", "position": "LW", "target": "Under 3.5 Shots on Goal Ceiling", "is_floor": False}
        ],
        "morale": [{"unit": "Predators Neutral Zone", "status": "WARN", "alert_text": "Game-Script Panic Threshold: High penalty minute risk trajectory modeled."}]
    },
    {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE",
        "game": "Utah Mammoth @ New Jersey Devils",
        "live_clock": "TONIGHT - 7:00 PM ET",
        "score_string": "0 - 0",
        "closing_line": "O/U 6.0",
        "sim_total": "Sim Total: 6.5",
        "pacing_status": "Pacing 🔥 OVER",
        "players": [
            {"name": "Jack Hughes", "position": "C", "target": "Over 3.5 Shots on Goal Floor", "is_floor": True},
            {"name": "Clayton Keller", "position": "LW", "target": "Under 2.5 Shots on Goal Ceiling", "is_floor": False}
        ],
        "morale": [{"unit": "Mammoth Blue Line", "status": "WARN", "alert_text": "Defensive structure fatigue penalty flagged on away sequence tracker."}]
    },
    {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE",
        "game": "Minnesota Wild @ Buffalo Sabres",
        "live_clock": "TONIGHT - 7:00 PM ET",
        "score_string": "0 - 0",
        "closing_line": "O/U 5.5",
        "sim_total": "Sim Total: 5.0",
        "pacing_status": "Pacing 📉 UNDER",
        "players": [
            {"name": "Kirill Kaprizov", "position": "LW", "target": "Over 3.5 Shots on Goal Floor", "is_floor": True},
            {"name": "Tage Thompson", "position": "C", "target": "Under 3.5 Shots on Goal Ceiling", "is_floor": False}
        ],
        "morale": [{"unit": "Sabres Offensive Flow", "status": "WARN", "alert_text": "High volume public backing on the over creates major contrarian value under."}]
    },
    {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE",
        "game": "St. Louis Blues @ Chicago Blackhawks",
        "live_clock": "TONIGHT - 8:00 PM ET",
        "score_string": "0 - 0",
        "closing_line": "O/U 5.5",
        "sim_total": "Sim Total: 6.0",
        "pacing_status": "Pacing 🔥 STABLE",
        "players": [
            {"name": "Connor Bedard", "position": "C", "target": "Over 3.5 Shots on Goal Floor", "is_floor": True},
            {"name": "Robert Thomas", "position": "C", "target": "Under 2.5 Shots on Goal Ceiling", "is_floor": False}
        ],
        "morale": [{"unit": "Blues Penalty Kill", "status": "WARN", "alert_text": "High expected box time trajectory. Connor Bedard powerplay insulation high."}]
    },
    {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE",
        "game": "Vegas Golden Knights @ Seattle Kraken",
        "live_clock": "TONIGHT - 9:40 PM ET",
        "score_string": "0 - 0",
        "closing_line": "O/U 5.5",
        "sim_total": "Sim Total: 5.5",
        "pacing_status": "Pacing 🔥 STABLE",
        "players": [
            {"name": "Jack Eichel", "position": "C", "target": "Over 3.5 Shots on Goal Floor", "is_floor": True},
            {"name": "Jared McCann", "position": "C", "target": "Under 2.5 Shots on Goal Ceiling", "is_floor": False}
        ],
        "morale": [
            {"unit": "Kraken Backcheck", "status": "WARN", "alert_text": "Increment Gain Strategy: Zone tracking identifies low volume under insulation."}
        ]
    },
    {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE",
        "game": "Florida Panthers @ Los Angeles Kings",
        "live_clock": "TONIGHT - 10:00 PM ET",
        "score_string": "0 - 0",
        "closing_line": "O/U 6.0",
        "sim_total": "Sim Total: 7.0",
        "pacing_status": "Pacing 💥 OVER",
        "players": [
            {"name": "Matthew Tkachuk", "position": "RW", "target": "Over 3.5 Shots on Goal Floor", "is_floor": True},
            {"name": "Anze Kopitar", "position": "C", "target": "Under 2.5 Shots on Goal Ceiling", "is_floor": False}
        ],
        "morale": [{"unit": "Kings Netminder Group", "status": "WARN", "alert_text": "Public Favorite Trap: High volume public backing exposure. High risk variance alert."}]
    },

    # ==========================================
    # 🏈 WEEK 5 CONTRARIAN NFL STRATEGY BOARDS (OCTOBER 8 - 12)
    # ==========================================
    {
        "sport_tag": "🏈 CONTRARIAN FOOTBALL SLATE",
        "game": "Tampa Bay Buccaneers @ Dallas Cowboys",
        "live_clock": "THU - 8:15 PM ET",
        "score_string": "PRE-GAME",
        "closing_line": "O/U 47.5",
        "sim_total": "CEE Projected: 49",
        "pacing_status": "Pacing 🔥 STABLE",
        "players": [
            {"name": "Dak Prescott", "position": "QB", "target": "Over 258.5 Passing Yards Floor", "is_floor": True},
            {"name": "CeeDee Lamb", "position": "WR", "target": "Under 7.5 Receptions Ceiling", "is_floor": False}
        ],
        "morale": [
            {"unit": "Buccaneers Front 7", "status": "WARN", "alert_text": "AWS Pass-Rush Score: Deficit tracked. Dak passing yard floor highly insulated."}
        ]
    },
    {
        "sport_tag": "🏈 CONTRARIAN FOOTBALL SLATE",
        "game": "Philadelphia Eagles @ Jacksonville Jaguars",
        "live_clock": "SUN - 9:30 AM ET",
        "score_string": "PRE-GAME",
        "closing_line": "O/U 46.5",
        "sim_total": "CEE Projected: 42",
        "pacing_status": "Pacing 📉 UNDER",
        "players": [
            {"name": "Saquon Barkley", "position": "RB", "target": "Over 78.5 Rushing Yards Floor", "is_floor": True},
            {"name": "DeVonta Smith", "position": "WR", "target": "Under 5.5 Receptions Ceiling", "is_floor": False}
        ],
        "morale": [{"unit": "Eagles Pass Block", "status": "WARN", "alert_text": "London Neutral Venue Filter: High travel fatigue tracking points directly to heavy run script."}]
    },
    {
        "sport_tag": "🏈 CONTRARIAN FOOTBALL SLATE",
        "game": "Chicago Bears @ Green Bay Packers",
        "live_clock": "SUN - 1:00 PM ET",
        "score_string": "PRE-GAME",
        "closing_line": "O/U 44.5",
        "sim_total": "CEE Projected: 41",
        "pacing_status": "Pacing 📉 UNDER",
        "players": [
            {"name": "D'Andre Swift", "position": "RB", "target": "Over 62.5 Rushing Yards Floor", "is_floor": True},
            {"name": "DJ Moore", "position": "WR", "target": "Under 5.5 Receptions Ceiling", "is_floor": False}
        ],
        "morale": [
            {"unit": "Packers Run Def", "status": "WARN", "alert_text": "Morale Deficit Flag engaged. Explosive public favorite trap bias active."}
        ]
    },
    {
        "sport_tag": "🏈 CONTRARIAN FOOTBALL SLATE",
        "game": "Minnesota Vikings @ New Orleans Saints",
        "live_clock": "SUN - 1:00 PM ET",
        "score_string": "PRE-GAME",
        "closing_line": "O/U 41.5",
        "sim_total": "CEE Projected: 46",
        "pacing_status": "Pacing 🔥 OVER",
        "players": [
