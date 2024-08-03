import os
import tempfile
import requests
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set up AI71 API details
AI71_BASE_URL = "https://api.ai71.ai/v1/"
AI71_API_KEY = "api71-api-8e137fd2-ae0f-4ce3-a682-a75c93b6d3ee"

# Initialize ChatOpenAI
chat = ChatOpenAI(
    model="tiiuae/falcon-180B-chat",
    api_key=AI71_API_KEY,
    base_url=AI71_BASE_URL,
)

# Function to send requests to AI71 API using ChatOpenAI
def ai71_request(prompt):
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=prompt),
    ]
    response = chat.invoke(messages)
    return response.content

# Define the tasks and their respective functions
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

# Streamlit setup
st.set_page_config(page_title="AI Legal Assistant", page_icon="⚖️")
st.title("⚖️ AI Legal Assistant")

# Function to reset chat history
def reset_chat_history():
    if 'langchain_messages' in st.session_state:
        del st.session_state['langchain_messages']

# Sidebar for task selection
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
    ],
    on_change=reset_chat_history
)

# Initialize chat history
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

view_messages = st.expander("View the message contents in session state")

# Task-specific UI and functionality
if task == "Simplifying Legal Documents":
    uploaded_file = st.file_uploader("Upload a legal document", type=["pdf"])
    if uploaded_file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                document_text = PyPDFLoader(temp_file.name).load()[0].page_content
                result = simplify_legal_documents(document_text)
                st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

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
    uploaded_file = st.file_uploader("Upload a contract", type=["pdf"])
    if uploaded_file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                document_text = PyPDFLoader(temp_file.name).load()[0].page_content
                result = contract_analysis(document_text)
                st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

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
    uploaded_file = st.file_uploader("Upload documents", type=["pdf"])
    if uploaded_file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                document_text = PyPDFLoader(temp_file.name).load()[0].page_content
                result = document_management(document_text)
                st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    prompt_chain = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an AI chatbot having a conversation with a human."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )
    chain = prompt_chain | chat
    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: msgs,
        input_messages_key="question",
        history_messages_key="history",
    )
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
