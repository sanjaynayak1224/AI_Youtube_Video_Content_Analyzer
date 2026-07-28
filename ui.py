import streamlit as st
from youtube_analyzer import build_youtube_agent


st.set_page_config(
    page_title="Youtube Video Analyzer",
    layout="centered"

)

st.title("📼AI Youtube Video Analyzer")


# Caching the agent for fast temporary access, stored in a temporary storage since it will be most frequently accessed

@st.cache_resource
def get_agent():
    return build_youtube_agent()


agent = get_agent()

# input box
video_url = st.text_input("Enter any Youtube Video's Link")  # stored as string
# The button is stored in the form of True or False
button = st.button("Analyze the Video")


if video_url and button:
    with st.spinner("Analyzing the Video..."):
        response = agent.run(
            f"Analyze this Video {video_url}",
        )
    st.markdown("Analysis Report for the Video")
    st.markdown(response.content)
