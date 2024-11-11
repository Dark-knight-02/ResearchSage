
import streamlit as st
from paper import get_arxiv_articles, download_and_merge_pdfs
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)

# Set page configuration
st.set_page_config(
    page_title="ResearchSage: Your Research Paper Assistant",
    page_icon=":books:",
    layout="wide",
)

# Sidebar with assistant description and instructions
with st.sidebar:
    st.title("ResearchSage")
    st.markdown("Your intelligent document assistant powered by OpenAI and LangChain.")
    st.markdown("---")
    st.markdown("**How to Use:**")
    st.markdown("1. Enter a topic you're interested in.")
    st.markdown("2. Specify a timeframe.")
    st.markdown("3. View research papers related to your topic.")
    st.markdown("---")

    # Settings container at the bottom
    st.title("⚙️ Settings")
    model_name = st.selectbox(
        "Choose Model:",
        options=["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4", "gpt-4o-mini", "chatgpt-4o-latest"]
    )
    st.markdown(f"Using Model {model_name}")

# Initialize session state variables
if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]
if 'requests' not in st.session_state:
    st.session_state['requests'] = []

# Main interface for user interaction
st.title("Research Paper Fetcher")
st.markdown("## Please enter the details to search for research papers")

# User input for topic
topic = st.text_input("What is the topic that you want to search about?", "")

# User input for timeframe
start_year = st.text_input("Start year (e.g., 2012):", "")
end_year = st.text_input("End year (e.g., 2015):", "")

# Fetch and display papers when user inputs both topic and timeframe
if st.button("Fetch Papers"):
    if topic and start_year and end_year:
        try:
            start_year, end_year = int(start_year), int(end_year)
            papers = get_arxiv_articles(topic, start_year, end_year)
            if papers:
                st.write("Here are the papers found:")
                for paper in papers:
                    st.markdown(f"- **{paper['title']}** by {paper['authors']} [Link]({paper['link']})")
                if st.button("Initiate chatbot"):
                    download_and_merge_pdfs([paper['link'] for paper in papers], topic)

                    
            else:
                st.warning("No papers found for the given criteria.")
        except ValueError:
            st.error("Please enter valid years.")
    else:
        st.error("Please enter both a topic and the timeframe.")
