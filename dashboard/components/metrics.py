"""Metrics display components"""

import streamlit as st
import pandas as pd
from utils.styling import create_metric_card
from utils.data_processing import calculate_win_rate, calculate_team_stats, get_home_away_stats

def display_overview_metrics(chelsea_overview, chelsea_matches):
    """Display key metrics for overview page"""
    if chelsea_overview.empty:
        st.error("No team data available")
        return
    
    team_info = chelsea_overview.iloc[0]
    win_rate, wins, total_matches = calculate_win_rate(chelsea_matches)
    upcoming_matches = len(chelsea_matches[chelsea_matches['status'].isin(['TIMED', 'SCHEDULED'])])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        premier_league_pos = team_info['premier_league_position'] if pd.notna(team_info['premier_league_position']) else 'N/A'
        premier_league_points = team_info['premier_league_points'] if pd.notna(team_info['premier_league_points']) else 0
        
        st.markdown(create_metric_card(
            "Premier League", 
            f"#{premier_league_pos}",
            f"{premier_league_points} points"
        ), unsafe_allow_html=True)
    
    with col2:
        champions_league_pos = team_info['champions_league_position'] if pd.notna(team_info['champions_league_position']) else 'N/A'
        champions_league_points = team_info['champions_league_points'] if pd.notna(team_info['champions_league_points']) else 0
        
        st.markdown(create_metric_card(
            "Champions League",
            f"#{champions_league_pos}",
            f"{champions_league_points} points"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card(
            "Win Rate",
            f"{win_rate:.1f}%",
            f"{wins}/{total_matches} matches"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card(
            "Upcoming",
            str(upcoming_matches),
            "fixtures"
        ), unsafe_allow_html=True)

def display_squad_metrics(chelsea_players):
    """Display squad statistics metrics"""
    if chelsea_players.empty:
        st.error("No player data available")
        return
    
    stats = calculate_team_stats(chelsea_players)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Players", stats['total_players'])
    with col2:
        st.metric("Average Age", f"{stats['avg_age']:.1f} years")
    with col3:
        st.metric("Nationalities", stats['nationalities'])
    with col4:
        st.metric("Different Positions", stats['positions'])

def display_home_away_metrics(chelsea_matches):
    """Display home vs away performance metrics"""
    stats = get_home_away_stats(chelsea_matches)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Home Win Rate", 
            f"{stats['home']['win_rate']:.1f}%",
            f"{stats['home']['wins']}/{stats['home']['total']} matches"
        )
    
    with col2:
        st.metric(
            "Away Win Rate", 
            f"{stats['away']['win_rate']:.1f}%",
            f"{stats['away']['wins']}/{stats['away']['total']} matches"
        )

def display_chelsea_position_highlight(standings_df):
    """Display Chelsea's position highlight in standings"""
    chelsea_position = standings_df[standings_df['team_name'] == 'Chelsea FC']
    
    if not chelsea_position.empty:
        pos = chelsea_position.iloc[0]
        st.success(f"🔵 Chelsea FC is currently in position **{pos['position']}** with **{pos['points']} points**")

def display_team_info_card(team_info):
    """Display team information card"""
    st.subheader("🏟️ Team Information")
    
    info_items = [
        ("Full Name", team_info['team_name']),
        ("Founded", team_info['founded']),
        ("Venue", team_info['venue']),
        ("Address", team_info['address']),
        ("Colors", team_info['club_colors']),
        ("Website", team_info['website'])
    ]
    
    for label, value in info_items:
        st.write(f"**{label}:** {value}")

def display_coaching_staff_card(team_info):
    """Display coaching staff information card"""
    st.subheader("👨‍💼 Coaching Staff")
    
    st.write(f"**Manager:** {team_info['coach_name']}")
    st.write(f"**Nationality:** {team_info['coach_nationality']}")
    
    if pd.notna(team_info['coach_contract_until']):
        st.write(f"**Contract Until:** {team_info['coach_contract_until']}")