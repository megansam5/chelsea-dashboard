"""Configuration settings for the Chelsea FC Dashboard"""

# Page configuration
PAGE_CONFIG = {
    "page_title": "Chelsea FC Data Dashboard",
    "page_icon": "⚽",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Sidebar configuration
SIDEBAR_CONFIG = {
    "logo_url": "https://crests.football-data.org/61.png",
    "logo_width": 100,
    "title": "Navigation"
}

# Database configuration - tables to load
TABLES = {
    "chelsea_overview": "mart_chelsea_overview",
    "chelsea_matches": "mart_chelsea_matches",
    "chelsea_players": "mart_chelsea_players",
    "competition_standings": "mart_competition_standings",
    "match_performance": "mart_match_performance"
}

# Chart colors
CHART_COLORS = {
    "chelsea_primary": "#034694",
    "chelsea_secondary": "#1e3d59",
    "win": "#28a745",
    "draw": "#ffc107",
    "loss": "#dc3545",
    "goals_scored": "#034694",
    "goals_conceded": "#ff6b35"
}

# Cache TTL (seconds)
CACHE_TTL = 600  # 10 minutes