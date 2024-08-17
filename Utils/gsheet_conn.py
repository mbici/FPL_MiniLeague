import streamlit as st
from streamlit_gsheets import GSheetsConnection
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import toml

@st.cache_data
def data_load(wksheet, cols):
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(worksheet=wksheet, usecols=cols)

    assert isinstance(data, object)
    data.reset_index(drop=True, inplace=True)
    return data


def update_data(wksheet, df):
    conn = st.connection("gsheets", type=GSheetsConnection)
    conn.update(worksheet=wksheet, data=df)

def load_credentials_from_secrets():
    secret = toml.load('.streamlit/secrets.toml')
    credentials_str = secret['google_sheets']['credentials']
    credentials_dict = json.loads(credentials_str)
    return credentials_dict


# Define your credentials and Google Sheet details
def authenticate_google_sheets():
    cred_dict = load_credentials_from_secrets()
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)
    client = gspread.authorize(credentials)
    return client