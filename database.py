from langchain.document_loaders import PyPDFDirectoryLoader

directory = 'arxiv_pdfs'

def load_docs(directory):
  loader = PyPDFDirectoryLoader(directory)
  documents = loader.load()
  return documents

docs = load_docs(directory)
print(len(docs))

from langchain.text_splitter import RecursiveCharacterTextSplitter
def chunk_data(doc, chunk_size=500, chunk_overlap=50):
    textsplitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    doc=textsplitter.split_documents(doc)
    return doc

documents = chunk_data(docs)

from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_docs(documents,chunk_size=500,chunk_overlap=50):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

import streamlit as st
docs = split_docs(documents)
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# import openai
from langchain.embeddings.openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os


PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "researpapers"


index = pc.create_index(
    name=index_name,
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)
docs = documents
from langchain_pinecone import PineconeVectorStore  
docsearch = PineconeVectorStore(index=index, embedding=embeddings,
                                pinecone_api_key=PINECONE_API_KEY,
                                index_name=index_name)

