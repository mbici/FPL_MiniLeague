import streamlit as st
from Utils.league import *


st.markdown(f'<h1 style="color:#33ff33;font-size:60px;background-image:linear-gradient(45deg, #1A512E, #63A91F);"'
            f'>FPL Mini-League Details App</h1>', unsafe_allow_html=True)
st.write('\n')

st.html(
    '''
    <style>
    hr {
        border-color: yellow;
    }
    </style>
    '''
)

st.markdown("""
<style>
.big-font {
    font-size:20px;
}
</style>
""", unsafe_allow_html=True)

st.divider()

_help = st.container(border=True)
_mgrDetails = st.container(border=True)

with _help:
    st.write('How to Use:')
    st.caption('Click on on the League Statistics menu option to get all statistics for Fantasy Kings - 2024/25')
    st.caption('Click on on the League Statistics menu option to get all managerial statistics from Fantasy Kings - 2024/25')

lg = league(140708)
lg_name = lg.get_league_name()

with _mgrDetails:
    st.write('\n')
    st.subheader(lg_name, anchor=False)

    st.markdown('<p class="big-font">Manager Details</p>', unsafe_allow_html=True)

    df = st.dataframe(lg.get_league_players(), hide_index=True, use_container_width=True, column_config={'Id': None},
                      column_order=['Player', 'Team'])

st.divider()

st.write('Support')
col1, col2 = st.columns([0.3, 4], gap="small", vertical_alignment="center")
with col1:
    st.image("./assets/profile_image.png", width=80)

with col2:
    st.caption("Himanshu Masani")
    st.caption('FPL Admin for Fantasy Kings 2024-25')
    if st.button("✉️ Contact Me"):
        st.warning('''
                - Phone : xxxxx
                - Email : test@test.com
                ''')