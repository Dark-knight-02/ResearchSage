import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from utils import *

# Set page configuration
st.set_page_config(
    page_title="ResearchSage: Your Research Paper Assistant",
    page_icon=":books:",
    layout="wide", 
)

# # Hide Streamlit style elements for a cleaner look
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True) 


# Sidebar with assistant description and instructions
with st.sidebar:
    st.title("ResearchSage")
    st.markdown("Your intelligent document assistant powered by OpenAI and LangChain.")
    st.markdown("---")
    st.markdown("**How to Use:**")
    st.markdown("1. Type your question related to your documents.")
    st.markdown("2. The assistant will provide accurate answers based on the context.")
    st.markdown("---")
    

    # Add a container for the settings at the bottom
    st.markdown('<div class="sidebar-settings">', unsafe_allow_html=True)

    st.title("⚙️ Settings")
    model_name = st.selectbox(
        "Choose Model:",
        options=["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4", "gpt-4o-mini", "chatgpt-4o-latest"]
    )
    st.markdown(f"Using Model {model_name}")
    # st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state variables
if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]
if 'requests' not in st.session_state:
    st.session_state['requests'] = []
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Set OpenAI API key from Streamlit secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Initialize the language model
llm = ChatOpenAI(model_name=model_name, openai_api_key=OPENAI_API_KEY)

# Define the prompt templates
system_msg_template = SystemMessagePromptTemplate.from_template(
    template="""Answer the question as truthfully as possible using the provided context, 
and if the answer is not contained within the text below, say 'I don't know'."""
)
human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

# Create the chat prompt template
prompt_template = ChatPromptTemplate.from_messages([
    system_msg_template,
    MessagesPlaceholder(variable_name="history"),
    human_msg_template
])

# Initialize the conversation chain
conversation = ConversationChain(
    llm=llm,
    prompt=prompt_template,
    memory=st.session_state.buffer_memory,
    verbose=True
)

# Main content area
st.title("ResearchSage: Your Research Article Assistant")

# Containers for chat interface
response_container = st.container()
text_container = st.container()

with text_container:
    query = st.text_input("Type your question here and press Enter:", key="input")
    if query:
        with st.spinner("Generating response..."):
            conversation_string = get_conversation_string()
            refined_query = query_refiner(conversation_string, query)
            context = find_match(refined_query)
            response = conversation.predict(
                input=f"Context:\n{context}\n\nQuery:\n{query}"
            )
        st.session_state.requests.append(query)
        st.session_state.responses.append(response)
        # Add messages to the conversation history
        st.session_state['messages'].append({"role": "user", "content": query})
        st.session_state['messages'].append({"role": "assistant", "content": response})

# Display chat history using Streamlit's chat elements
with response_container:
    for message in st.session_state['messages']:
        if message['role'] == 'assistant':
            with st.chat_message("assistant"):
                st.markdown(message['content']) 
        else:
            with st.chat_message("user"):
                st.markdown(message['content'])

# Optionally, add a button to clear the conversation
if st.button("Clear Conversation"):
    st.session_state['messages'] = []
    st.session_state['requests'] = []
    st.session_state['responses'] = ["How can I assist you?"]
    st.session_state.buffer_memory.clear()
    st.session_state.clear()
    # st.experimental_rerun()