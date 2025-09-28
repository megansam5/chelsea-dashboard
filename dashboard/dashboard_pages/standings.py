"""League standings page for the Chelsea FC Dashboard"""

import streamlit as st
import pandas as pd
from components.tables import display_standings_table
from components.metrics import display_chelsea_position_highlight
from utils.data_processing import get_competition_list, filter_by_competition

def show_page(data):
    """Display the league standings page"""
    competition_standings = data.get('competition_standings', pd.DataFrame())
    
    st.subheader("📊 League Standings")
    
    if competition_standings.empty:
        st.error("No standings data available")
        return
    
    # Competition selector
    competitions = competition_standings['competition'].unique()
    selected_competition = st.selectbox("Select Competition", competitions)
    
    # Filter standings by selected competition
    filtered_standings = competition_standings[
        competition_standings['competition'] == selected_competition
    ]
    
    # Display standings table
    display_standings_table(filtered_standings)
    
    # Highlight Chelsea's position
    display_chelsea_position_highlight(filtered_standings)