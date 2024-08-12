import streamlit as st
from streamlit_gsheets import GSheetsConnection


@st.cache_data
def data_load(wksheet, cols):
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(worksheet=wksheet, usecols=cols)

    assert isinstance(data, object)
    data.reset_index(drop=True, inplace=True)
    return data
