import streamlit as st
import requests
import os
import tempfile
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.text_splitter import RecursiveCharacterTextSplitter

st.set_page_config(page_title="AI Legal Assistant", page_icon="⚖️")
st.title("⚖️ AI Legal Assistant")

AI71_BASE_URL = "https://api.ai71.ai/v1/"
AI71_API_KEY = "api71-api-8e137fd2-ae0f-4ce3-a682-a75c93b6d3ee"

# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

view_messages = st.expander("View the message contents in session state")

# Function to read PDF files
def read_pdf(file_path):
    with fitz.open(file_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# Function to read DOCX files
def read_docx(file_path):
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Function to process the file based on its type
def process_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        with open("temp_file.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        return read_pdf("temp_file.pdf")
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        with open("temp_file.docx", "wb") as f:
            f.write(uploaded_file.getbuffer())
        return read_docx("temp_file.docx")
    else:
        return None

# Define the tasks and their respective functions
def ai71_request(prompt):
    headers = {
        "Authorization": f"Bearer {AI71_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "tiiuae/falcon-180b-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(f"{AI71_BASE_URL}chat/completions", headers=headers, json=data)
    response_data = response.json()
    return response_data['choices'][0]['message']['content']

def simplify_legal_documents(document_text):
    prompt = f"Simplify the following legal document: {document_text}"
    return ai71_request(prompt)

def predictive_analytics(case_details):
    prompt = f"Predict the outcome of the following case: {case_details}"
    return ai71_request(prompt)

def automated_legal_research(query):
    prompt = f"Search and provide relevant legal precedents, statutes, and regulations for: {query}"
    return ai71_request(prompt)

def contract_analysis(document_text):
    prompt = f"Analyze the following contract for potential risks and compliance issues: {document_text}"
    return ai71_request(prompt)

def contract_drafting(context):
    prompt = f"Draft a contract based on the following context: {context}"
    return ai71_request(prompt)

def access_legal_services(query):
    prompt = f"Provide preliminary legal advice for: {query}"
    return ai71_request(prompt)

def regulatory_compliance_monitoring(query):
    prompt = f"Monitor and provide alerts for regulatory changes related to: {query}"
    return ai71_request(prompt)

def bias_detection(query):
    prompt = f"Analyze the following legal data for bias: {query}"
    return ai71_request(prompt)

def policy_analysis(query):
    prompt = f"Simulate the potential impacts of the following policy: {query}"
    return ai71_request(prompt)

def document_management(document_text):
    prompt = f"Sort and analyze the following documents: {document_text}"
    return ai71_request(prompt)

# Streamlit app
st.title("AI-Powered Legal Assistant")
st.sidebar.title("Choose a Task")

task = st.sidebar.selectbox(
    "Select a task",
    [
        "Simplifying Legal Documents",
        "Predictive Analytics in Legal Decisions",
        "Automated Legal Research",
        "Contract Analysis and Management",
        "Contract Drafting",
        "Access to Legal Services",
        "Regulatory Compliance Monitoring",
        "Bias Detection and Mitigation",
        "Data-Driven Policy Making",
        "Document Management and e-Discovery"
    ]
)

if task == "Simplifying Legal Documents":
    uploaded_file = st.file_uploader("Upload a legal document", type=["pdf", "docx"])
    if uploaded_file is not None:
        document_text = process_file(uploaded_file)
        if document_text:
            result = simplify_legal_documents(document_text)
            st.write(result)
        else:
            st.error("Unsupported file type.")

elif task == "Predictive Analytics in Legal Decisions":
    case_details = st.text_area("Enter case details")
    if st.button("Predict Outcome"):
        result = predictive_analytics(case_details)
        st.write(result)

elif task == "Automated Legal Research":
    query = st.text_area("Enter your research query")
    if st.button("Search"):
        result = automated_legal_research(query)
        st.write(result)

elif task == "Contract Analysis and Management":
    uploaded_file = st.file_uploader("Upload a contract", type=["pdf", "docx"])
    if uploaded_file is not None:
        document_text = process_file(uploaded_file)
        if document_text:
            result = contract_analysis(document_text)
            st.write(result)
        else:
            st.error("Unsupported file type.")

elif task == "Contract Drafting":
    context = st.text_area("Enter context for contract drafting")
    if st.button("Draft Contract"):
        result = contract_drafting(context)
        st.write(result)

elif task == "Access to Legal Services":
    query = st.text_area("Enter your legal query")
    if st.button("Get Advice"):
        result = access_legal_services(query)
        st.write(result)

elif task == "Regulatory Compliance Monitoring":
    query = st.text_area("Enter query for regulatory compliance monitoring")
    if st.button("Monitor"):
        result = regulatory_compliance_monitoring(query)
        st.write(result)

elif task == "Bias Detection and Mitigation":
    query = st.text_area("Enter data for bias detection")
    if st.button("Detect Bias"):
        result = bias_detection(query)
        st.write(result)

elif task == "Data-Driven Policy Making":
    query = st.text_area("Enter policy details for analysis")
    if st.button("Analyze Policy"):
        result = policy_analysis(query)
        st.write(result)

elif task == "Document Management and e-Discovery":
    uploaded_file = st.file_uploader("Upload documents", type=["pdf", "docx"])
    if uploaded_file is not None:
        document_text = process_file(uploaded_file)
        if document_text:
            result = document_management(document_text)
            st.write(result)
        else:
            st.error("Unsupported file type.")

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    # Note: new messages are saved to history automatically by Langchain during run
    config = {"configurable": {"session_id": "any"}}
    response = chain_with_history.invoke({"question": prompt}, config)
    st.chat_message("ai").write(response.content)

# Draw the messages at the end, so newly generated ones show up immediately
with view_messages:
    """
    Message History initialized with:
    ```python
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    ```

    Contents of `st.session_state.langchain_messages`:
    """
    view_messages.json(st.session_state.langchain_messages)
