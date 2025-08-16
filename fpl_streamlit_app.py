import streamlit as st
from pathlib import Path

st.set_page_config(layout="wide")

# --- CUSTOM CSS INJECTION ---
with open("assets/custom_sidebar.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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
myspace = st.Page(
    'views/myspace.py',
    title='My Space',
    icon=':material/groups:',
)

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Welcome": [about_page],
        "Menu": [league, analytics, myspace],
    }
)

# --- SHARED ON ALL PAGES ---
st.logo("assets/fpl.png")

# --- RUN NAVIGATION ---
pg.run()