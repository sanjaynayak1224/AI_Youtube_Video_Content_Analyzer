import streamlit as st
from youtube_analyzer import build_youtube_agent


st.set_page_config(
    page_title="Youtube Video Analyzer",
    page_icon="📼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for modern UI aesthetic
st.markdown("""
    <style>
    .main .block-container {
        max-width: 1000px;
        padding-top: 2rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%);
        color: white;
        font-weight: 600;
        height: 46px;
        border: none;
        box-shadow: 0 4px 12px rgba(255, 0, 0, 0.25);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #FF1A1A 0%, #E60000 100%);
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(255, 0, 0, 0.35);
    }
    </style>
""", unsafe_allow_html=True)

st.title("📼AI Youtube Video Analyzer")
st.caption("🚀 Instant AI Summaries, Key Takeaways & Timestamped Topics powered by Agno & Groq")

# Sidebar with Instructions & Features
with st.sidebar:
    st.header("⚙️ About & Usage")
    st.markdown("""
    This application uses AI agents to automatically analyze YouTube video content, creating structured summaries, topic progressions, and precise timestamps.
    
    **How to use:**
    1. Paste a public YouTube video URL into the input field.
    2. Click **Analyze the Video**.
    3. Review the video preview and generated report below.
    """)
    st.divider()
    st.markdown("💡 *Tip: Works best with educational videos, technical tutorials, product reviews, and lectures.*")


# Caching the agent for fast temporary access, stored in a temporary storage since it will be most frequently accessed

@st.cache_resource
def get_agent():
    return build_youtube_agent()


agent = get_agent()

col1, col2 = st.columns([3, 1])

with col1:
    # input box
    video_url = st.text_input("Enter any Youtube Video's Link", placeholder="https://www.youtube.com/watch?v=...")  # stored as string

with col2:
    st.write("##")
    # The button is stored in the form of True or False
    button = st.button("Analyze the Video", type="primary")


if video_url:
    # Embedded Video Preview
    with st.expander("📺 Video Preview", expanded=not button):
        try:
            st.video(video_url)
        except Exception:
            st.info("Preview unavailable for this URL format, but analysis can still proceed.")

if video_url and button:
    with st.spinner("Analyzing the Video..."):
        try:
            response = agent.run(
                f"Analyze this Video {video_url}",
            )
            st.markdown("---")
            st.markdown("### 📊 Analysis Report for the Video")
            
            # Extract content safely
            content = getattr(response, "content", str(response))
            st.markdown(content)

            # Allow downloading the report as Markdown
            st.download_button(
                label="📥 Download Analysis Report (.md)",
                data=content,
                file_name="youtube_video_analysis.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"❌ An error occurred during analysis: {str(e)}")
            st.info("Please verify your YouTube link and ensure your `GROQ_API_KEY` is configured correctly in `.env`.")
elif button and not video_url:
    st.warning("⚠️ Please enter a valid YouTube video URL first.")
