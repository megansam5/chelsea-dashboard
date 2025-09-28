"""Table display components"""

import streamlit as st
import pandas as pd
from utils.data_processing import format_match_date, prepare_standings_display

def display_standings_table(standings_df):
    """Display league standings table"""
    if standings_df.empty:
        st.info("No standings data available")
        return
    
    display_df = prepare_standings_display(standings_df)
    
    st.dataframe(
        display_df,
        column_config={
            "position": st.column_config.NumberColumn("Pos", width="small"),
            "team_name": st.column_config.TextColumn("Team"),
            "played_games": st.column_config.NumberColumn("P", width="small"),
            "won": st.column_config.NumberColumn("W", width="small"),
            "draw": st.column_config.NumberColumn("D", width="small"),
            "lost": st.column_config.NumberColumn("L", width="small"),
            "goals_for": st.column_config.NumberColumn("GF", width="small"),
            "goals_against": st.column_config.NumberColumn("GA", width="small"),
            "goal_difference": st.column_config.NumberColumn("GD", width="small"),
            "points": st.column_config.NumberColumn("Pts", width="small"),
            "form": st.column_config.TextColumn("Form", width="medium")
        },
        hide_index=True,
        use_container_width=True
    )

def display_matches_table(matches_df, title, show_results=True):
    """Display matches table with configurable columns"""
    if matches_df.empty:
        st.info(f"No {title.lower()} available")
        return
    
    # Prepare display columns
    display_cols = ['match_date', 'competition_name', 'opponent', 'venue_type']
    if show_results:
        display_cols.extend(['chelsea_goals', 'opponent_goals', 'result'])
    else:
        display_cols.append('status')
    
    # Format the dataframe for display
    display_df = matches_df[display_cols].copy()
    display_df['match_date'] = display_df['match_date'].apply(format_match_date)
    
    # Configure columns
    column_config = {
        "match_date": st.column_config.TextColumn("Date"),
        "competition_name": st.column_config.TextColumn("Competition"),
        "opponent": st.column_config.TextColumn("Opponent"),
        "venue_type": st.column_config.TextColumn("Venue")
    }
    
    if show_results:
        column_config.update({
            "chelsea_goals": st.column_config.NumberColumn("Chelsea", width="small"),
            "opponent_goals": st.column_config.NumberColumn("Opponent", width="small"),
            "result": st.column_config.TextColumn("Result")
        })
    else:
        column_config["status"] = st.column_config.TextColumn("Status")
    
    st.dataframe(
        display_df,
        column_config=column_config,
        hide_index=True,
        use_container_width=True
    )

def display_squad_table(players_df):
    """Display squad players table"""
    if players_df.empty:
        st.error("No player data available")
        return
    
    st.dataframe(
        players_df[['player_name', 'position', 'age', 'nationality']],
        column_config={
            "player_name": st.column_config.TextColumn("Player Name"),
            "position": st.column_config.TextColumn("Position"),
            "age": st.column_config.NumberColumn("Age", width="small"),
            "nationality": st.column_config.TextColumn("Nationality")
        },
        hide_index=True,
        use_container_width=True
    )

def display_performance_metrics_table(match_performance):
    """Display detailed performance metrics table"""
    if match_performance.empty:
        st.info("No performance data available")
        return
    
    st.dataframe(
        match_performance[[
            'competition_name', 'total_matches', 'wins', 'draws', 'losses',
            'goals_scored', 'goals_conceded', 'goal_difference', 
            'points_percentage', 'last_5_form'
        ]],
        column_config={
            "competition_name": st.column_config.TextColumn("Competition"),
            "total_matches": st.column_config.NumberColumn("Matches", width="small"),
            "wins": st.column_config.NumberColumn("W", width="small"),
            "draws": st.column_config.NumberColumn("D", width="small"),
            "losses": st.column_config.NumberColumn("L", width="small"),
            "goals_scored": st.column_config.NumberColumn("GF", width="small"),
            "goals_conceded": st.column_config.NumberColumn("GA", width="small"),
            "goal_difference": st.column_config.NumberColumn("GD", width="small"),
            "points_percentage": st.column_config.NumberColumn("Points %", format="%.1f%%"),
            "last_5_form": st.column_config.TextColumn("Last 5", width="medium")
        },
        hide_index=True,
        use_container_width=True
    )