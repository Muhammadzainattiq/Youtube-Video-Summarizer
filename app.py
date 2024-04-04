import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
st.set_page_config(page_title="Yt video summarizer", page_icon="📝")
st.markdown("""
    <style>
        .header {
            font-size: 56px;
            color: #FDFEFF; /* Change the color as per your preference */
            background-color: #f50000;
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2); /* Add shadow effect */
        }
        .head {
            font-size: 16px;
            color: #FDFEFF; /* Change the color as per your preference */
            background-color: #f50000;
            text-align: left;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2); /* Add shadow effect */
        }
        .response {
            font-size: 34px;
            color: red; /* Change the color as per your preference */
            text-align: left;
            margin-bottom: 20px;
        }
        
    </style>
""", unsafe_allow_html=True)
created_style = """
    color: #888888; /* Light gray color */
    font-size: 99px; /* Increased font size */
""" 

genai.configure(api_key= st.secrets["GOOGLE_API_KEY"])
prompt = """You are a youtube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important summary in points.
Ensure that your summary is clear, concise, and captures the essence of the video effectively. Avoid including unnecessary details or tangential information. Your goal is to provide a comprehensive yet succinct overview of the video's content.The transcript text is here: 
"""
def generate_gemini_content(transcript, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript)
    return response.text


def extract_transcript(video_id):
    """Extracts the transcript from a YouTube video."""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        for transcript in transcript_list:
            transcript_text_list = transcript.fetch()
            lang = transcript.language
            transcript_text = ""
            if transcript.language_code == 'en':
                for line in transcript_text_list:
                    transcript_text += " " + line["text"]
                return transcript_text
            elif transcript.is_translatable:
                english_transcript_list = transcript.translate('en').fetch()
                for line in english_transcript_list:
                    transcript_text += " " + line["text"]
                return transcript_text
        st.info("Transcript extraction failed. Please check the video URL.")
    except Exception as e:
        st.info(f"Error: {e}")


         
st.markdown("<p style='{}'>➡️created by 'Muhammad Zain Attiq'</p>".format(created_style), unsafe_allow_html=True)
st.markdown('<h1 class="header">Youtube Video Summarizer </h1>', unsafe_allow_html=True)
with st.expander("About the app..."):
    st.markdown('<h1 class="head">What the App Can Do: </h1>', unsafe_allow_html=True)
    st.write("The YouTube Video Summarizer extracts transcripts from YouTube videos, summarizes them, and presents important points. It automatically detects the language and translates non-English transcripts to English. Users can preview videos, access transcripts, and get concise summaries in real-time.")

    st.markdown('<h1 class="head">How to use this app: </h1>', unsafe_allow_html=True)
    st.markdown("""
    1. Input the YouTube video URL.
2. Preview the video.
3. Click "Get Summary" to extract the transcript and generate the summary.
4. View the summarized content, which captures the essence of the video effectively.

Developed by Muhammad Zain Attiq, the app offers a simple yet powerful tool for summarizing video content based on transcripts.
""")


video_url = st.text_input("Enter the video link: ")

if video_url:
    video_id = video_url.split("=")[1]
    st.video(video_url)
submit = st.button("Get Summary")
if submit:
    with st.spinner("Extracting Transcript..."):
        transcript = extract_transcript(video_id)
    if transcript:
        with st.spinner("Generating Summary..."):
            summary = generate_gemini_content(transcript, prompt)
        st.markdown('<h1 class="response">Summary: </h1>', unsafe_allow_html=True)
        st.write(summary)
        st.write("__________________________________________________________________________________")