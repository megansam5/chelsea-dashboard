import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import psycopg2
from dotenv import load_dotenv
from psycopg2 import extras
import os
from os import environ as ENV
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Chelsea FC Data Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database connection
@st.cache_resource
def init_connection():
    load_dotenv()
    return psycopg2.connect(dbname=ENV["DB_NAME"],
                            host=ENV["DB_HOST"],
                            user=ENV["DB_USER"],
                            port=ENV["DB_PORT"],
                            password=ENV["DB_PASSWORD"],
                            cursor_factory=psycopg2.extras.RealDictCursor)


# Load data (cached for 10 minutes)
@st.cache_data(ttl=600)
def load_data(table_name):
    conn = init_connection()
    table_and_schema = 'analytics.' + table_name
    query = f"SELECT * FROM {table_and_schema}"
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()  # list of dicts
    return pd.DataFrame(rows)  # convert to DataFrame

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

def main():
    # Load data
    try:
        chelsea_overview = load_data("mart_chelsea_overview")
        chelsea_matches = load_data("mart_chelsea_matches")
        chelsea_players = load_data("mart_chelsea_players")
        competition_standings = load_data("mart_competition_standings")
        match_performance = load_data("mart_match_performance")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

    # Sidebar
    st.sidebar.image("https://logos-world.net/wp-content/uploads/2020/06/Chelsea-Logo.png", width=100)
    st.sidebar.title("Navigation")
    
    pages = ["🏠 Overview", "📊 League Standings", "⚽ Matches", "👥 Squad", "📈 Performance Analytics"]
    selected_page = st.sidebar.selectbox("Select Page", pages)

    # Main header
    if not chelsea_overview.empty:
        team_info = chelsea_overview.iloc[0]
        st.markdown(f"""
        <div class="team-header">
            <h1>🔵 {team_info['team_name']} Dashboard</h1>
            <p>Founded: {team_info['founded']} | Venue: {team_info['venue']} | Coach: {team_info['coach_name']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Page routing
    if selected_page == "🏠 Overview":
        show_overview_page(chelsea_overview, chelsea_matches, match_performance)
    elif selected_page == "📊 League Standings":
        show_standings_page(competition_standings, chelsea_overview)
    elif selected_page == "⚽ Matches":
        show_matches_page(chelsea_matches)
    elif selected_page == "👥 Squad":
        show_squad_page(chelsea_players)
    elif selected_page == "📈 Performance Analytics":
        show_analytics_page(chelsea_matches, match_performance)

def show_overview_page(chelsea_overview, chelsea_matches, match_performance):
    if chelsea_overview.empty:
        st.error("No team data available")
        return
    
    team_info = chelsea_overview.iloc[0]
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h3>Premier League</h3>
            <h2>#{team_info['premier_league_position'] if pd.notna(team_info['premier_league_position']) else 'N/A'}</h2>
            <p>{team_info['premier_league_points'] if pd.notna(team_info['premier_league_points']) else 0} points</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h3>Champions League</h3>
            <h2>#{team_info['champions_league_position'] if pd.notna(team_info['champions_league_position']) else 'N/A'}</h2>
            <p>{team_info['champions_league_points'] if pd.notna(team_info['champions_league_points']) else 0} points</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_matches = len(chelsea_matches[chelsea_matches['status'] == 'FINISHED'])
        wins = len(chelsea_matches[(chelsea_matches['status'] == 'FINISHED') & (chelsea_matches['result'] == 'Win')])
        win_rate = (wins / total_matches * 100) if total_matches > 0 else 0
        st.markdown(f"""
        <div class="metric-container">
            <h3>Win Rate</h3>
            <h2>{win_rate:.1f}%</h2>
            <p>{wins}/{total_matches} matches</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        upcoming_matches = len(chelsea_matches[chelsea_matches['status'].isin(['TIMED', 'SCHEDULED'])])
        st.markdown(f"""
        <div class="metric-container">
            <h3>Upcoming</h3>
            <h2>{upcoming_matches}</h2>
            <p>fixtures</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Team details and recent matches
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🏟️ Team Information")
        st.write(f"**Full Name:** {team_info['team_name']}")
        st.write(f"**Founded:** {team_info['founded']}")
        st.write(f"**Venue:** {team_info['venue']}")
        st.write(f"**Address:** {team_info['address']}")
        st.write(f"**Colors:** {team_info['club_colors']}")
        st.write(f"**Website:** {team_info['website']}")
        
        st.subheader("👨‍💼 Coaching Staff")
        st.write(f"**Manager:** {team_info['coach_name']}")
        st.write(f"**Nationality:** {team_info['coach_nationality']}")
        if pd.notna(team_info['coach_contract_until']):
            st.write(f"**Contract Until:** {team_info['coach_contract_until']}")
    
    with col2:
        st.subheader("📅 Recent Matches")
        recent_matches = chelsea_matches[chelsea_matches['status'] == 'FINISHED'].head(5)
        
        for _, match in recent_matches.iterrows():
            result_class = f"match-result-{match['result'].lower()}"
            match_date = pd.to_datetime(match['match_date']).strftime('%d/%m/%Y')
            
            st.markdown(f"""
            <div class="{result_class}">
                <strong>{match_date}</strong> - {match['competition_name']}<br>
                {match['opponent']} ({match['venue_type']}) - {match['result']}<br>
                Score: {match['chelsea_goals']}-{match['opponent_goals']}
            </div>
            """, unsafe_allow_html=True)
    
    # Performance summary
    if not match_performance.empty:
        st.subheader("🏆 Season Performance Summary")
        
        fig = go.Figure()
        competitions = match_performance['competition_name'].tolist()
        wins = match_performance['wins'].tolist()
        draws = match_performance['draws'].tolist()
        losses = match_performance['losses'].tolist()
        
        fig.add_trace(go.Bar(name='Wins', x=competitions, y=wins, marker_color='#28a745'))
        fig.add_trace(go.Bar(name='Draws', x=competitions, y=draws, marker_color='#ffc107'))
        fig.add_trace(go.Bar(name='Losses', x=competitions, y=losses, marker_color='#dc3545'))
        
        fig.update_layout(
            title="Match Results by Competition",
            xaxis_title="Competition",
            yaxis_title="Number of Matches",
            barmode='stack',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_standings_page(competition_standings, chelsea_overview):
    st.subheader("📊 League Standings")
    
    # Competition selector
    competitions = competition_standings['competition'].unique()
    selected_competition = st.selectbox("Select Competition", competitions)
    
    # Filter standings
    filtered_standings = competition_standings[competition_standings['competition'] == selected_competition]
    
    # Display standings table
    st.dataframe(
        filtered_standings[['position', 'team_name', 'played_games', 'won', 'draw', 'lost', 
                          'goals_for', 'goals_against', 'goal_difference', 'points', 'form']],
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
    
    # Highlight Chelsea's position
    chelsea_position = filtered_standings[filtered_standings['team_name'] == 'Chelsea FC']
    if not chelsea_position.empty:
        pos = chelsea_position.iloc[0]
        st.success(f"🔵 Chelsea FC is currently in position **{pos['position']}** with **{pos['points']} points**")

def show_matches_page(chelsea_matches):
    st.subheader("⚽ Match Center")
    
    # Match type selector
    match_tabs = st.tabs(["📈 All Matches", "✅ Past Matches", "📅 Upcoming Matches"])
    
    with match_tabs[0]:
        show_matches_table(chelsea_matches, "All Matches")
    
    with match_tabs[1]:
        past_matches = chelsea_matches[chelsea_matches['status'] == 'FINISHED']
        show_matches_table(past_matches, "Past Matches")
    
    with match_tabs[2]:
        upcoming_matches = chelsea_matches[chelsea_matches['status'].isin(['TIMED', 'SCHEDULED'])]
        show_matches_table(upcoming_matches, "Upcoming Matches", show_results=False)

def show_matches_table(matches_df, title, show_results=True):
    if matches_df.empty:
        st.info(f"No {title.lower()} available")
        return
    
    # Competition filter
    competitions = ['All'] + sorted(matches_df['competition_name'].unique().tolist())
    selected_comp = st.selectbox(f"Filter by Competition ({title})", competitions, key=f"comp_{title}")
    
    if selected_comp != 'All':
        matches_df = matches_df[matches_df['competition_name'] == selected_comp]
    
    # Display columns
    display_cols = ['match_date', 'competition_name', 'opponent', 'venue_type']
    if show_results:
        display_cols.extend(['chelsea_goals', 'opponent_goals', 'result'])
    else:
        display_cols.append('status')
    
    # Format the dataframe for display
    display_df = matches_df[display_cols].copy()
    display_df['match_date'] = pd.to_datetime(display_df['match_date']).dt.strftime('%d/%m/%Y')
    
    st.dataframe(
        display_df,
        column_config={
            "match_date": st.column_config.TextColumn("Date"),
            "competition_name": st.column_config.TextColumn("Competition"),
            "opponent": st.column_config.TextColumn("Opponent"),
            "venue_type": st.column_config.TextColumn("Venue"),
            "chelsea_goals": st.column_config.NumberColumn("Chelsea", width="small"),
            "opponent_goals": st.column_config.NumberColumn("Opponent", width="small"),
            "result": st.column_config.TextColumn("Result"),
            "status": st.column_config.TextColumn("Status")
        },
        hide_index=True,
        use_container_width=True
    )

def show_squad_page(chelsea_players):
    st.subheader("👥 Chelsea FC Squad")
    
    if chelsea_players.empty:
        st.error("No player data available")
        return
    
    # Position filter
    positions = ['All'] + sorted(chelsea_players['position_category'].unique().tolist())
    selected_position = st.selectbox("Filter by Position", positions)
    
    if selected_position != 'All':
        filtered_players = chelsea_players[chelsea_players['position_category'] == selected_position]
    else:
        filtered_players = chelsea_players
    
    # Squad statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Players", len(chelsea_players))
    with col2:
        avg_age = chelsea_players['age'].mean()
        st.metric("Average Age", f"{avg_age:.1f} years")
    with col3:
        nationalities = chelsea_players['nationality'].nunique()
        st.metric("Nationalities", nationalities)
    with col4:
        positions_count = chelsea_players['position'].nunique()
        st.metric("Different Positions", positions_count)
    
    # Players table
    st.dataframe(
        filtered_players[['player_name', 'position', 'age', 'nationality']],
        column_config={
            "player_name": st.column_config.TextColumn("Player Name"),
            "position": st.column_config.TextColumn("Position"),
            "age": st.column_config.NumberColumn("Age", width="small"),
            "nationality": st.column_config.TextColumn("Nationality")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Age distribution chart
    fig = px.histogram(
        chelsea_players, 
        x='age', 
        nbins=15,
        title="Age Distribution of Squad",
        labels={'age': 'Age', 'count': 'Number of Players'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Position breakdown
    position_counts = chelsea_players['position_category'].value_counts()
    fig_pie = px.pie(
        values=position_counts.values,
        names=position_counts.index,
        title="Squad Breakdown by Position Category"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

def show_analytics_page(chelsea_matches, match_performance):
    st.subheader("📈 Performance Analytics")
    
    # Goals analysis
    finished_matches = chelsea_matches[chelsea_matches['status'] == 'FINISHED'].copy()
    
    if finished_matches.empty:
        st.info("No completed matches available for analysis")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Goals scored vs conceded over time
        finished_matches['match_date'] = pd.to_datetime(finished_matches['match_date'])
        finished_matches = finished_matches.sort_values('match_date')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=finished_matches['match_date'],
            y=finished_matches['chelsea_goals'],
            mode='lines+markers',
            name='Goals Scored',
            line=dict(color='#28a745')
        ))
        fig.add_trace(go.Scatter(
            x=finished_matches['match_date'],
            y=finished_matches['opponent_goals'],
            mode='lines+markers',
            name='Goals Conceded',
            line=dict(color='#dc3545')
        ))
        
        fig.update_layout(
            title="Goals Scored vs Conceded Over Time",
            xaxis_title="Date",
            yaxis_title="Goals",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Results distribution
        result_counts = finished_matches['result'].value_counts()
        colors = {'Win': '#28a745', 'Draw': '#ffc107', 'Loss': '#dc3545'}
        fig_results = px.pie(
            values=result_counts.values,
            names=result_counts.index,
            title="Match Results Distribution",
            color=result_counts.index,
            color_discrete_map=colors
        )
        fig_results.update_layout(height=400)
        st.plotly_chart(fig_results, use_container_width=True)
    
    # Performance by competition
    if not match_performance.empty:
        st.subheader("Competition Performance Comparison")
        
        fig = go.Figure()
        competitions = match_performance['competition_name']
        
        fig.add_trace(go.Bar(
            name='Goals Scored',
            x=competitions,
            y=match_performance['goals_scored'],
            marker_color='#034694'
        ))
        
        fig.add_trace(go.Bar(
            name='Goals Conceded',
            x=competitions,
            y=match_performance['goals_conceded'],
            marker_color='#ff6b35'
        ))
        
        fig.update_layout(
            title="Goals Scored vs Conceded by Competition",
            xaxis_title="Competition",
            yaxis_title="Goals",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance metrics table
        st.subheader("Detailed Performance Metrics")
        st.dataframe(
            match_performance[['competition_name', 'total_matches', 'wins', 'draws', 'losses',
                             'goals_scored', 'goals_conceded', 'goal_difference', 'points_percentage', 'last_5_form']],
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

    # Home vs Away performance
    home_matches = finished_matches[finished_matches['venue_type'] == 'Home']
    away_matches = finished_matches[finished_matches['venue_type'] == 'Away']
    
    if not home_matches.empty and not away_matches.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            home_wins = len(home_matches[home_matches['result'] == 'Win'])
            home_total = len(home_matches)
            home_win_rate = (home_wins / home_total * 100) if home_total > 0 else 0
            
            st.metric(
                "Home Win Rate", 
                f"{home_win_rate:.1f}%",
                f"{home_wins}/{home_total} matches"
            )
        
        with col2:
            away_wins = len(away_matches[away_matches['result'] == 'Win'])
            away_total = len(away_matches)
            away_win_rate = (away_wins / away_total * 100) if away_total > 0 else 0
            
            st.metric(
                "Away Win Rate", 
                f"{away_win_rate:.1f}%",
                f"{away_wins}/{away_total} matches"
            )

if __name__ == "__main__":
    main()