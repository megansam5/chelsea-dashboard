"""Performance analytics page for the Chelsea FC Dashboard"""

import streamlit as st
import pandas as pd
from components.charts import (
    create_goals_timeline_chart,
    create_results_pie_chart,
    create_goals_by_competition_chart
)
from components.tables import display_performance_metrics_table
from components.metrics import display_home_away_metrics

def show_page(data):
    """Display the analytics page"""
    chelsea_matches = data.get('chelsea_matches', pd.DataFrame())
    match_performance = data.get('match_performance', pd.DataFrame())
    
    st.subheader("📈 Performance Analytics")
    
    # Check if we have completed matches for analysis
    finished_matches = chelsea_matches[chelsea_matches['status'] == 'FINISHED']
    
    if finished_matches.empty:
        st.info("No completed matches available for analysis")
        return
    
    # Goals analysis section
    display_goals_analysis_section(finished_matches)
    
    # Competition performance section
    if not match_performance.empty:
        display_competition_performance_section(match_performance)
    
    # Home vs Away performance section
    display_home_away_section(chelsea_matches)

def display_goals_analysis_section(finished_matches):
    """Display goals analysis charts"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Goals timeline chart
        timeline_chart = create_goals_timeline_chart(finished_matches)
        if timeline_chart:
            st.plotly_chart(timeline_chart, use_container_width=True)
    
    with col2:
        # Results distribution pie chart
        results_chart = create_results_pie_chart(finished_matches)
        if results_chart:
            st.plotly_chart(results_chart, use_container_width=True)

def display_competition_performance_section(match_performance):
    """Display competition performance analysis"""
    st.subheader("Competition Performance Comparison")
    
    # Goals by competition chart
    goals_chart = create_goals_by_competition_chart(match_performance)
    if goals_chart:
        st.plotly_chart(goals_chart, use_container_width=True)
    
    # Performance metrics table
    st.subheader("Detailed Performance Metrics")
    display_performance_metrics_table(match_performance)

def display_home_away_section(chelsea_matches):
    """Display home vs away performance section"""
    st.subheader("Home vs Away Performance")
    
    # Display home vs away metrics
    display_home_away_metrics(chelsea_matches)