"""Overview page for the Chelsea FC Dashboard"""

import streamlit as st
import pandas as pd
from components.metrics import (
    display_overview_metrics, 
    display_team_info_card, 
    display_coaching_staff_card
)
from components.charts import create_performance_bar_chart
from utils.styling import create_match_result_card
from utils.data_processing import get_recent_matches

def show_page(data):
    """Display the overview page"""
    chelsea_overview = data.get('chelsea_overview', pd.DataFrame())
    chelsea_matches = data.get('chelsea_matches', pd.DataFrame())
    match_performance = data.get('match_performance', pd.DataFrame())
    
    if chelsea_overview.empty:
        st.error("No team data available")
        return
    
    team_info = chelsea_overview.iloc[0]
    
    # Display key metrics
    display_overview_metrics(chelsea_overview, chelsea_matches)
    
    # Team details and recent matches
    col1, col2 = st.columns([1, 1])
    
    with col1:
        display_team_info_card(team_info)
        st.markdown("---")
        display_coaching_staff_card(team_info)
    
    with col2:
        display_recent_matches_section(chelsea_matches)
    
    # Performance summary chart
    display_performance_summary_section(match_performance)

def display_recent_matches_section(chelsea_matches):
    """Display recent matches section"""
    st.subheader("📅 Recent Matches")
    
    recent_matches = get_recent_matches(chelsea_matches, limit=5)
    
    if recent_matches.empty:
        st.info("No recent matches available")
        return
    
    for _, match in recent_matches.iterrows():
        match_date = pd.to_datetime(match['match_date']).strftime('%d/%m/%Y')
        
        match_info = {
            'date': match_date,
            'competition': match['competition_name'],
            'opponent': match['opponent'],
            'venue': match['venue_type'],
            'result': match['result'],
            'chelsea_goals': match['chelsea_goals'],
            'opponent_goals': match['opponent_goals']
        }
        
        st.markdown(create_match_result_card(match_info), unsafe_allow_html=True)

def display_performance_summary_section(match_performance):
    """Display performance summary section"""
    if match_performance.empty:
        st.info("No performance data available")
        return
    
    st.subheader("🏆 Season Performance Summary")
    
    # Create and display performance chart
    fig = create_performance_bar_chart(match_performance)
    if fig:
        st.plotly_chart(fig, use_container_width=True)