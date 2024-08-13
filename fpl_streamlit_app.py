import streamlit as st

st.set_page_config(layout="wide")
# --- PAGE SETUP ---
about_page = st.Page(
    'views/about_me.py',
    title='Get Started',
    icon=':material/info:',
    default=True,
)
league = st.Page(
    'views/minileague.py',
    title='League Statistics',
    icon=':material/emoji_events:',
)
analytics = st.Page(
    'views/analytics.py',
    title='Manager Statistics',
    icon=':material/analytics:'
)

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Welcome": [about_page],
        "Menu": [league, analytics],
    }
)

# --- SHARED ON ALL PAGES ---
st.logo("assets/fpl.png")

# --- RUN NAVIGATION ---
pg.run()