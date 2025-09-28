"""Matches page for the Chelsea FC Dashboard"""

import streamlit as st
import pandas as pd
from components.tables import display_matches_table
from utils.data_processing import (
    get_competition_list, 
    filter_by_competition,
    get_upcoming_matches
)

def show_page(data):
    """Display the matches page"""
    chelsea_matches = data.get('chelsea_matches', pd.DataFrame())
    
    st.subheader("⚽ Match Center")
    
    if chelsea_matches.empty:
        st.error("No matches data available")
        return
    
    # Create tabs for different match views
    match_tabs = st.tabs(["📈 All Matches", "✅ Past Matches", "📅 Upcoming Matches"])
    
    with match_tabs[0]:
        show_matches_section(chelsea_matches, "All Matches", show_results=True)
    
    with match_tabs[1]:
        past_matches = chelsea_matches[chelsea_matches['status'] == 'FINISHED']
        show_matches_section(past_matches, "Past Matches", show_results=True)
    
    with match_tabs[2]:
        upcoming_matches = get_upcoming_matches(chelsea_matches)
        show_matches_section(upcoming_matches, "Upcoming Matches", show_results=False)

def show_matches_section(matches_df, title, show_results=True):
    """Display a matches section with competition filter"""
    if matches_df.empty:
        st.info(f"No {title.lower()} available")
        return
    
    # Competition filter
    competitions = get_competition_list(matches_df, 'competition_name')
    selected_comp = st.selectbox(
        f"Filter by Competition ({title})", 
        competitions, 
        key=f"comp_{title.replace(' ', '_')}"
    )
    
    # Filter by selected competition
    filtered_matches = filter_by_competition(matches_df, selected_comp, 'competition_name')
    
    # Display matches table
    display_matches_table(filtered_matches, title, show_results)