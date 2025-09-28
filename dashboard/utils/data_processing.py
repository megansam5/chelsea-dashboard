"""Data processing utilities"""

import pandas as pd
from datetime import datetime

def calculate_win_rate(matches_df):
    """Calculate win rate from matches dataframe"""
    if matches_df.empty:
        return 0, 0, 0
    
    finished_matches = matches_df[matches_df['status'] == 'FINISHED']
    total_matches = len(finished_matches)
    wins = len(finished_matches[finished_matches['result'] == 'Win'])
    win_rate = (wins / total_matches * 100) if total_matches > 0 else 0
    
    return win_rate, wins, total_matches

def get_recent_matches(matches_df, limit=5):
    """Get recent finished matches"""
    finished_matches = matches_df[matches_df['status'] == 'FINISHED']
    return finished_matches.head(limit)

def get_upcoming_matches(matches_df):
    """Get upcoming matches"""
    return matches_df[matches_df['status'].isin(['TIMED', 'SCHEDULED'])]

def format_match_date(date_str):
    """Format match date for display"""
    try:
        return pd.to_datetime(date_str).strftime('%d/%m/%Y')
    except:
        return date_str

def calculate_team_stats(players_df):
    """Calculate team statistics from players dataframe"""
    if players_df.empty:
        return {
            'total_players': 0,
            'avg_age': 0,
            'nationalities': 0,
            'positions': 0
        }
    
    return {
        'total_players': len(players_df),
        'avg_age': players_df['age'].mean(),
        'nationalities': players_df['nationality'].nunique(),
        'positions': players_df['position'].nunique()
    }

def get_home_away_stats(matches_df):
    """Calculate home vs away performance statistics"""
    finished_matches = matches_df[matches_df['status'] == 'FINISHED']
    
    home_matches = finished_matches[finished_matches['venue_type'] == 'Home']
    away_matches = finished_matches[finished_matches['venue_type'] == 'Away']
    
    def calculate_stats(df):
        if df.empty:
            return {'wins': 0, 'total': 0, 'win_rate': 0}
        
        wins = len(df[df['result'] == 'Win'])
        total = len(df)
        win_rate = (wins / total * 100) if total > 0 else 0
        
        return {'wins': wins, 'total': total, 'win_rate': win_rate}
    
    return {
        'home': calculate_stats(home_matches),
        'away': calculate_stats(away_matches)
    }

def prepare_standings_display(standings_df):
    """Prepare standings dataframe for display"""
    if standings_df.empty:
        return standings_df
    
    display_columns = [
        'position', 'team_name', 'played_games', 'won', 'draw', 'lost',
        'goals_for', 'goals_against', 'goal_difference', 'points', 'form'
    ]
    
    return standings_df[display_columns]

def get_competition_list(df, column='competition_name'):
    """Get sorted list of competitions with 'All' option"""
    if df.empty:
        return ['All']
    
    competitions = sorted(df[column].unique().tolist())
    return ['All'] + competitions

def filter_by_competition(df, competition, column='competition_name'):
    """Filter dataframe by competition"""
    if competition == 'All':
        return df
    return df[df[column] == competition]