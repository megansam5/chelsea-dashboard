import streamlit as st
from config.settings import PAGE_CONFIG, SIDEBAR_CONFIG
from database.db_manager import DataManager
from utils.styling import load_custom_css
from dashboard_pages import overview, standings, matches, squad, analytics

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Load custom styling
load_custom_css()

def main():
    """Main application function"""
    
    # Initialize data manager
    try:
        data_manager = DataManager()
        data = data_manager.load_all_data()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

    # Sidebar configuration
    st.sidebar.image(SIDEBAR_CONFIG["logo_url"], width=SIDEBAR_CONFIG["logo_width"])
    st.sidebar.title(SIDEBAR_CONFIG["title"])
    
    # Navigation
    pages = {
        "🏠 Overview": overview,
        "📊 League Standings": standings,
        "⚽ Matches": matches,
        "👥 Squad": squad,
        "📈 Performance Analytics": analytics
    }
    
    selected_page = st.sidebar.selectbox("Select Page", list(pages.keys()))
    
    # Display team header
    display_team_header(data.get('chelsea_overview'))
    
    # Route to selected page
    if selected_page in pages:
        pages[selected_page].show_page(data)

def display_team_header(chelsea_overview):
    """Display the main team header"""
    if chelsea_overview is not None and not chelsea_overview.empty:
        team_info = chelsea_overview.iloc[0]
        st.markdown(f"""
        <div class="team-header">
            <h1>🔵 {team_info['team_name']} Dashboard</h1>
            <p>Founded: {team_info['founded']} | Venue: {team_info['venue']} | Coach: {team_info['coach_name']}</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()