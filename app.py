import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Billboard Top 5",
    page_icon="🎧",
    layout="centered"
)

# Custom CSS for a fresh appearance
st.markdown(
    """
    <style>
    .hit-card {
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
        border-left: 6px solid #ff4081;
    }
    .title {
        font-size: 20px;
        color: #444444;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .artist {
        color: #888;
        font-size: 16px;
        margin-bottom: 10px;
    }
    .spotify-link {
        display: flex;
        justify-content: center;
        margin-top: 15px;
    }
    .stButton>button {
        background-color: #ff4081  ;
        color: #ffffff  ;
        border-radius: 20px  ;
        border: none  ;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎧 Billboard Hits Explorer")

# Function to filter top songs
def filter_top_songs(df, month, year):
    df['chart_week'] = pd.to_datetime(df['chart_week'])
    filtered = df[(df['chart_week'].dt.month == month) & (df['chart_week'].dt.year == year)]
    if filtered.empty:
        return None
    latest_week = filtered['chart_week'].max()
    return filtered[filtered['chart_week'] == latest_week].head(5)

# Load data
try:
    data = pd.read_csv('billboards.csv')
    data['chart_week'] = pd.to_datetime(data['chart_week'])

    st.sidebar.header("🎛️ Choose Date")

    year_selected = st.sidebar.selectbox("Year", sorted(data['chart_week'].dt.year.unique(), reverse=True))
    month_selected = st.sidebar.selectbox("Month", range(1, 13), format_func=lambda x: datetime(2000, x, 1).strftime('%B'))

    top_hits = filter_top_songs(data, month_selected, year_selected)

    if top_hits is not None:
        st.header(f"Top 5 Songs for {datetime(year_selected, month_selected, 1).strftime('%B %Y')}")

        for index, hit in top_hits.iterrows():
            st.markdown(
                f"""
                <div class='hit-card'>
                    <div class='title'>{hit['title']}</div>
                    <div class='artist'>🎤 {hit['performer']} | Position: #{hit['current_week']}</div>
                    <div class='spotify-link'>
                """,
                unsafe_allow_html=True
            )

            if pd.notna(hit['spotify_link']):
                st.link_button("Play on Spotify 🎶", hit['spotify_link'])
            else:
                st.markdown("<span style='color: #f44336;'>Spotify link unavailable.</span>", unsafe_allow_html=True)

            st.markdown("</div></div>", unsafe_allow_html=True)

    else:
        st.warning("No songs found for the chosen date.")

except FileNotFoundError:
    st.error("File 'billboards.csv' not found. Ensure it is in the correct directory.")
