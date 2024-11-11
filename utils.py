import os
import pinecone
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import openai
from langchain.embeddings.openai import OpenAIEmbeddings
import streamlit as st
from pinecone import ServerlessSpec

# Set API keys from Streamlit secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
PINECONE_ENVIRONMENT = st.secrets["PINECONE_ENVIRONMENT"]

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Initialize the pinecone index
index_name = "researchpapers"
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(index_name) 


def find_match(input_text):
    # Generate OpenAI embeddings
    response = openai.Embedding.create(
        input=input_text,
        model="text-embedding-ada-002"
    )
    input_em = response['data'][0]['embedding']
    # Query Pinecone index
    result = index.query(vector=input_em, top_k=2, include_metadata=True)
    matches = result['matches']
    if len(matches) >= 2:
        return matches[0]['metadata']['text'] + "\n" + matches[1]['metadata']['text']
    elif len(matches) == 1:
        return matches[0]['metadata']['text']
    else:
        return "I'm sorry, I couldn't find any relevant information."

def query_refiner(conversation, query):
    """
    Refines a user query by rephrasing it into a standalone question using the OpenAI API.

    Parameters:
    - conversation (str): The conversation history.
    - query (str): The user's current query.

    Returns:
    - refined_query (str): The refined standalone question.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that helps to rephrase follow-up questions into standalone questions."},
            {"role": "user", "content": f"Given the following conversation and a follow-up question, rephrase the question to be a standalone question.\n\nConversation:\n{conversation}\n\nFollow-up Question:\n{query}\n\nStandalone question:"}
        ],
        temperature=0.7,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    refined_query = response['choices'][0]['message']['content'].strip()
    return refined_query

def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses']) - 1):
        conversation_string += "Human: " + st.session_state['requests'][i] + "\n"
        conversation_string += "Assistant: " + st.session_state['responses'][i + 1] + "\n"
    return conversation_string
