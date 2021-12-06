import streamlit as st
import pandas as pd
import numpy as np
from google.oauth2 import service_account
from gsheetsdb import connect


st.title('Stanford Behavior Design - Emotion Regulation Tool')

st.caption(
    "The following questions will help us match you with the best technique.")
environment = st.selectbox(
    'Which of the following best describes a situation when you need more positive emotions?',
    ('Waking up', 'At work', 'At home alone', 'At home with family or friends', 'About to go to bed'))
emotion = st.selectbox(
    'Which of the following best describes your emotional state when you need more positive emotions?',
    ('Tired and unmotivated', 'Overwhelmed', 'Bored', 'Just "normal"', 'Sad', 'Stressed', 'Restless'))


# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)


@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows


sheet_url = st.secrets["gsheets"]["Beta_Tool_Data"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')


################################
