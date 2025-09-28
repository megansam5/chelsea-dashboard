"""Squad page for the Chelsea FC Dashboard"""

import streamlit as st
import pandas as pd
from components.metrics import display_squad_metrics
from components.tables import display_squad_table
from components.charts import create_age_distribution_chart, create_position_breakdown_chart
from utils.data_processing import get_competition_list, filter_by_competition

def show_page(data):
    """Display the squad page"""
    chelsea_players = data.get('chelsea_players', pd.DataFrame())
    
    st.subheader("👥 Chelsea FC Squad")
    
    if chelsea_players.empty:
        st.error("No player data available")
        return
    
    # Position filter
    positions = get_competition_list(chelsea_players, 'position_category')
    selected_position = st.selectbox("Filter by Position", positions)
    
    # Filter players by position
    if selected_position != 'All':
        filtered_players = chelsea_players[
            chelsea_players['position_category'] == selected_position
        ]
    else:
        filtered_players = chelsea_players
    
    # Display squad metrics
    display_squad_metrics(chelsea_players)
    
    # Display squad table
    st.subheader("📋 Squad List")
    display_squad_table(filtered_players)
    
    # Display charts
    display_squad_charts(chelsea_players)

def display_squad_charts(chelsea_players):
    """Display squad analysis charts"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Age distribution chart
        age_chart = create_age_distribution_chart(chelsea_players)
        if age_chart:
            st.plotly_chart(age_chart, use_container_width=True)
    
    with col2:
        # Position breakdown chart
        position_chart = create_position_breakdown_chart(chelsea_players)
        if position_chart:
            st.plotly_chart(position_chart, use_container_width=True)