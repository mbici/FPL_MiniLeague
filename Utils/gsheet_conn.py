import streamlit as st
from streamlit_gsheets import GSheetsConnection
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import toml


def data_load(wksheet, cols):
    """
    Function to load data from a googlesheet into a pandas dataframe
    :param wksheet: Worksheet name
    :param cols: Columns to be considered in the sheet
    :return: pandas dataframe of values from the sheet
    """
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(worksheet=wksheet, usecols=cols)

    assert isinstance(data, object)
    data.reset_index(drop=True, inplace=True)
    return data


def update_data(wksheet, df):
    """
    Function to update data in the googlesheet
    :param wksheet: Worksheet Name
    :param df: pandas Dataframe to be updated into the sheet
    :return:
    """
    conn = st.connection("gsheets", type=GSheetsConnection)
    conn.update(worksheet=wksheet, data=df)


def load_credentials_from_secrets():
    """
    Function to laod credentials from the secrets toml file
    :return: dictionary of the secret values
    """
    secret = toml.load('.streamlit/secrets.toml')
    credentials_str = secret['google_sheets']['credentials']
    credentials_dict = json.loads(credentials_str)
    return credentials_dict


def authenticate_google_sheets():
    """
    Authenticating google_sheet connection
    :return: returns a connection client
    """
    cred_dict = load_credentials_from_secrets()
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)
    client = gspread.authorize(credentials)
    return client
