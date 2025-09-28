"""Chart components for the dashboard"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config.settings import CHART_COLORS

def create_performance_bar_chart(match_performance):
    """Create stacked bar chart for match performance by competition"""
    if match_performance.empty:
        return None
    
    fig = go.Figure()
    competitions = match_performance['competition_name'].tolist()
    wins = match_performance['wins'].tolist()
    draws = match_performance['draws'].tolist()
    losses = match_performance['losses'].tolist()
    
    fig.add_trace(go.Bar(name='Wins', x=competitions, y=wins, 
                        marker_color=CHART_COLORS['win']))
    fig.add_trace(go.Bar(name='Draws', x=competitions, y=draws, 
                        marker_color=CHART_COLORS['draw']))
    fig.add_trace(go.Bar(name='Losses', x=competitions, y=losses, 
                        marker_color=CHART_COLORS['loss']))
    
    fig.update_layout(
        title="Match Results by Competition",
        xaxis_title="Competition",
        yaxis_title="Number of Matches",
        barmode='stack',
        height=400
    )
    
    return fig

def create_goals_timeline_chart(matches_df):
    """Create timeline chart for goals scored vs conceded"""
    finished_matches = matches_df[matches_df['status'] == 'FINISHED'].copy()
    
    if finished_matches.empty:
        return None
    
    finished_matches['match_date'] = pd.to_datetime(finished_matches['match_date'])
    finished_matches = finished_matches.sort_values('match_date')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=finished_matches['match_date'],
        y=finished_matches['chelsea_goals'],
        mode='lines+markers',
        name='Goals Scored',
        line=dict(color=CHART_COLORS['win'])
    ))
    fig.add_trace(go.Scatter(
        x=finished_matches['match_date'],
        y=finished_matches['opponent_goals'],
        mode='lines+markers',
        name='Goals Conceded',
        line=dict(color=CHART_COLORS['loss'])
    ))
    
    fig.update_layout(
        title="Goals Scored vs Conceded Over Time",
        xaxis_title="Date",
        yaxis_title="Goals",
        height=400
    )
    
    return fig

def create_results_pie_chart(matches_df):
    """Create pie chart for match results distribution"""
    finished_matches = matches_df[matches_df['status'] == 'FINISHED']
    
    if finished_matches.empty:
        return None
    
    result_counts = finished_matches['result'].value_counts()
    colors = [CHART_COLORS['win'], CHART_COLORS['draw'], CHART_COLORS['loss']]
    
    fig = px.pie(
        values=result_counts.values,
        names=result_counts.index,
        title="Match Results Distribution",
        color=result_counts.index,
        color_discrete_map={
            'Win': CHART_COLORS['win'],
            'Draw': CHART_COLORS['draw'],
            'Loss': CHART_COLORS['loss']
        }
    )
    fig.update_layout(height=400)
    
    return fig

def create_goals_by_competition_chart(match_performance):
    """Create grouped bar chart for goals by competition"""
    if match_performance.empty:
        return None
    
    fig = go.Figure()
    competitions = match_performance['competition_name']
    
    fig.add_trace(go.Bar(
        name='Goals Scored',
        x=competitions,
        y=match_performance['goals_scored'],
        marker_color=CHART_COLORS['goals_scored']
    ))
    
    fig.add_trace(go.Bar(
        name='Goals Conceded',
        x=competitions,
        y=match_performance['goals_conceded'],
        marker_color=CHART_COLORS['goals_conceded']
    ))
    
    fig.update_layout(
        title="Goals Scored vs Conceded by Competition",
        xaxis_title="Competition",
        yaxis_title="Goals",
        barmode='group',
        height=400
    )
    
    return fig

def create_age_distribution_chart(players_df):
    """Create histogram for player age distribution"""
    if players_df.empty:
        return None
    
    fig = px.histogram(
        players_df, 
        x='age', 
        nbins=15,
        title="Age Distribution of Squad",
        labels={'age': 'Age', 'count': 'Number of Players'},
        color_discrete_sequence=[CHART_COLORS['chelsea_primary']]
    )
    fig.update_layout(height=400)
    
    return fig

def create_position_breakdown_chart(players_df):
    """Create pie chart for squad position breakdown"""
    if players_df.empty:
        return None
    
    position_counts = players_df['position_category'].value_counts()
    
    fig = px.pie(
        values=position_counts.values,
        names=position_counts.index,
        title="Squad Breakdown by Position Category",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    return fig