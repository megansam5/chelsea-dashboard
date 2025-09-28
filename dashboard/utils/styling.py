"""Styling utilities and CSS definitions"""

import streamlit as st

def load_custom_css():
    """Load custom CSS styles"""
    st.markdown("""
    <style>
        .metric-container {
            background-color: #1e3d59;
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem;
        }
        
        .team-header {
            background: linear-gradient(90deg, #1e3d59 0%, #034694 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .competition-card {
            border: 2px solid #034694;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            background-color: #f8f9fa;
        }
        
        .match-result-win {
            background-color: #d4edda;
            border-left: 5px solid #28a745;
            padding: 0.5rem;
            margin: 0.25rem 0;
        }
        
        .match-result-draw {
            background-color: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 0.5rem;
            margin: 0.25rem 0;
        }
        
        .match-result-loss {
            background-color: #f8d7da;
            border-left: 5px solid #dc3545;
            padding: 0.5rem;
            margin: 0.25rem 0;
        }
        
        .info-card {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .stat-highlight {
            font-size: 1.2em;
            font-weight: bold;
            color: #034694;
        }
    </style>
    """, unsafe_allow_html=True)

def create_metric_card(title, value, subtitle=None):
    """Create a styled metric card"""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    
    return f"""
    <div class="metric-container">
        <h3>{title}</h3>
        <h2>{value}</h2>
        {subtitle_html}
    </div>
    """

def create_match_result_card(match_info):
    """Create a styled match result card"""
    result_class = f"match-result-{match_info['result'].lower()}"
    
    return f"""
    <div class="{result_class}">
        <strong>{match_info['date']}</strong> - {match_info['competition']}<br>
        {match_info['opponent']} ({match_info['venue']}) - {match_info['result']}<br>
        Score: {match_info['chelsea_goals']}-{match_info['opponent_goals']}
    </div>
    """