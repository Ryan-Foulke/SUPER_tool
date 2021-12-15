from re import X
import streamlit as st
import pandas as pd
import numpy as np
from google.oauth2 import service_account
from gsheetsdb import connect


# Create connection to google sheets data.
###############################################################

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


def get_data():
    sheet_url = st.secrets["gsheets"]["Beta_Tool_Data"]
    rows = run_query(f'SELECT * FROM "{sheet_url}"')
    return(pd.DataFrame(rows))


# Matching Tool
############################################################

def get_random_technique(environment, emotion):
    techniques = get_data()
    suggested_technique = techniques[techniques.Environment.eq(
        environment)][techniques.Emotion.eq(emotion)].Technique.values[0]
    return(suggested_technique)


def matching_page_3():
    placeholder = st.empty()
    with placeholder.container():
        st.header('Stanford Behavior Design: Emotion Regulation Tool')
        st.markdown("Your target behavior:")
        st.markdown("**" + st.session_state.user['behavior'] + "**")
        st.markdown("")
        st.markdown("**Todo:**")
        task_1 = st.checkbox(
            "Write down your target behavior somewhere where you will remember it.")
        task_2 = st.checkbox("Set up your prompt: " +
                             st.session_state.user['prompt'])
        task_3 = st.checkbox("Set aside your time to reflect on this behavior: " +
                             st.session_state.user['reflection'])
        if(task_1 and task_2 and task_3):
            st.balloons()
            st.markdown(
                "Congratulations on taking a step towards more positive emotions in your life!")
            st.caption("Let us know how it goes by using the _Report Results_ tab or engage with other people trying to up regulate positive emotions using the _Community_ tab.")


def matching_page_2():
    placeholder = st.empty()
    with placeholder.container():
        environment = st.session_state.user['environment']
        emotion = st.session_state.user['emotion']
        technique = st.session_state.user['technique']
        st.header('Stanford Behavior Design: Emotion Regulation Tool')
        full_behavior = "When I am " + environment.lower() + " and feeling " + \
            emotion.lower() + ", I will " + technique.lower()
        st.session_state.user['behavior'] = st.text_area(
            "How could you make this behavior more specific to talor it to your paticular situation?", value=full_behavior, height=2)
        st.session_state.user['prompt'] = st.text_input(
            "What would be a good prompt to remind you to do this behavior?")
        st.session_state.user['reflection'] = st.text_input(
            "When would you have time to reflect and iterate on how this behavior is working?")
        if(st.button("Next", key=(st.session_state.user['tab'] + str(st.session_state.user['subpage'])))):
            st.session_state.user['subpage'] = 3
            placeholder.empty()


def matching_page_1():
    environment = st.session_state.user['environment']
    emotion = st.session_state.user['emotion']
    technique = st.session_state.user['technique']
    placeholder = st.empty()
    with placeholder.container():
        st.header('Stanford Behavior Design: Emotion Regulation Tool')
        st.markdown('For your situation, _' +
                    environment.lower() + " and feeling " + emotion.lower() + '_, we recommend the following behavior:')
        st.markdown('**' + technique + "**")
        st.caption("Finding the right behavior for your situation is just the first step. Next, we will help you implement this behavior in your daily routine.")
        if(st.button("Next", key=(st.session_state.user['tab'] + str(st.session_state.user['subpage'])))):
            st.session_state.user['subpage'] = 2
            placeholder.empty()


def matching_page_0():
    placeholder = st.empty()
    with placeholder.container():
        st.header('Stanford Behavior Design: Emotion Regulation Tool')
        st.caption(
            "The purpose of this tool is to match you with behaviors that will help you feel more positive emotions in in your daily life. These behaviors are based on a combination of research in the field of emotion regulation and data collected by our lab.")
        st.caption(
            "The following questions will help us match you with the best behavior.")
        st.session_state.user['environment'] = st.selectbox(
            'Which of the following best describes the environment when you need more positive emotions?',
            ('Waking up', 'At work', 'At home alone', 'At home with family or friends', 'About to go to bed'), key="test")
        st.session_state.user['emotion'] = st.selectbox(
            'Which of the following best describes your emotional state when you need more positive emotions?',
            ('Tired and unmotivated', 'Overwhelmed', 'Bored', 'Just "normal"', 'Sad', 'Stressed', 'Restless'))
        st.session_state.user['technique'] = get_random_technique(
            st.session_state.user['environment'], st.session_state.user['emotion'])
        if(st.button("Next", key=(st.session_state.user['tab'] + str(st.session_state.user['subpage'])))):
            st.session_state.user['subpage'] = 1
            placeholder.empty()


def show_matching_tool():
    if(st.session_state.user['subpage'] == 0):
        matching_page_0()

    if(st.session_state.user['subpage'] == 1):
        matching_page_1()

    if(st.session_state.user['subpage'] == 2):
        matching_page_2()
    if(st.session_state.user['subpage'] == 3):
        matching_page_3()


def results_page_1():
    placeholder = st.empty()
    with placeholder.container():
        st.header('Stanford Behavior Design: Emotion Regulation Tool')
        st.caption(
            "The Stanford Behavior Design Lab is striving to understand the behaviors we can use to introduce more positive emotions in day to day life. Reporting the success of your target behavior will help us advace this research and help more people.")
        techniques = get_data().Technique.to_numpy()
        techniques = np.insert(techniques, 0, [""])
        behavior = st.selectbox(
            'Which of the following was the target behavior recommended to you? (Search using key words)',
            techniques, 0, help="Search using key words")
        st.radio(
            "How often did you use this behavior?", ["Never", "Almost never", "Sometimes", "Almost every time", "Every time"], index=2)
        st.radio(
            "How difficult was this behavior to do?", ["Very difficult", "Difficult", "Neutral", "Easy", "Very easy"], index=2)
        st.radio(
            "What level of impact did this behavior have on your positive emotions?", ["Very low", "Low", "Medium", "High", "Very High"], index=2)

        if(st.button("Submit")):
            st.session_state.user['subpage'] = 1
            placeholder.empty()


def results_page_2():
    st.header('Stanford Behavior Design: Emotion Regulation Tool')
    st.markdown("**Thank you for your feedback**")
    st.markdown(
        "This will help us advance our research and continue to make the tool better in the future.")
    st.caption(
        "Please contact behaviordesign@stanford.edu with any additional questions or feedback.")


def show_report_results():
    if(st.session_state.user['subpage'] == 0):
        results_page_1()

    if(st.session_state.user['subpage'] == 1):
        results_page_2()


def show_community():
    st.header('Stanford Behavior Design: Emotion Regulation Tool')
    st.write("Coming Soon")


def hide_top_bar():
    hide_decoration_bar_style = '''<style> header {visibility: hidden;} </style>'''
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)


################################
def main():
    hide_top_bar()

    # Initialize user session
    if('user' not in st.session_state):
        st.session_state['user'] = ({
            "tab": "Matching Tool",
            "subpage": 0,
        })

    # Siderbar Navigation
    st.sidebar.header("Navigation")
    st.session_state.user["tab"] = st.sidebar.radio(
        "Go to",
        ("Matching Tool", "Report Results", "Community")
    )

    if(st.session_state.user["tab"] == "Matching Tool"):
        show_matching_tool()
    if(st.session_state.user["tab"] == "Report Results"):
        st.session_state.user['subpage'] = 0
        show_report_results()
    if(st.session_state.user["tab"] == "Community"):
        st.session_state.user['subpage'] = 0
        show_community()


if __name__ == "__main__":
    main()
