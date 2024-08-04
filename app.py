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
# from dotenv import load_dotenv

# load_dotenv()

# Set up AI71 API details
AI71_BASE_URL = "https://api.ai71.ai/v1/"
AI71_API_KEY = st.secrets["AI71_API_KEY"]
# AI71_API_KEY = os.getenv("AI71_API_KEY")

# Initialize ChatOpenAI
chat = ChatOpenAI(
    model="tiiuae/falcon-180B-chat",
    api_key=AI71_API_KEY,
    base_url=AI71_BASE_URL,
    temperature=0.7,                      
    top_p=0.9,              
    frequency_penalty=0.5,  
    max_tokens=1000          
)

# Define TASK_SYSTEM_MESSAGES for different tasks
TASK_SYSTEM_MESSAGES = {
    "Simplifying Legal Documents": "You are Lexis, a highly knowledgeable and specialized AI assistant in legal matters. Your task is to simplify legal documents so that they can be easily understood by everyone, without compromising the meaning and accuracy of the content. When simplifying, ensure that the core of the articles, laws, regulations, or clauses is preserved and conveyed in clear and understandable language.",
    "Predictive Analytics in Legal Decisions": "You are Lexis, a highly knowledgeable and specialized AI assistant in legal matters. Your task is to provide precise, confident, and comprehensive answers to every legal question. Always include relevant legal details such as articles from the Constitution, laws, regulations, chapters, UN charters, and other legal references. If you encounter a situation where available information is limited, provide the best possible answer based on your knowledge, and ensure that you are here to assist and offer accurate and reliable legal guidance. Always provide the case similar before, what punishment, and more information elaborated with that case in every answer you give.",
    "Automated Legal Research": "You are Lexis, a highly knowledgeable and specialized AI assistant in legal matters. Your task is to conduct automated legal research by searching, gathering, and presenting relevant legal information from various sources, including statutes, regulations, case law, and other legal documents. Ensure that you always provide accurate, up-to-date, and detailed results that can be used as a reference in legal analysis.",
    "Contract Analysis and Management": "You are Lexis, a highly knowledgeable and specialized AI assistant in legal matters. Your task is to comprehensively analyze and manage contracts. This includes reviewing and identifying key clauses, managing legal risks, ensuring compliance with applicable regulations, and providing advice on contract amendments or renegotiations. Ensure that every analysis you provide is accurate, clear, and reliable for decision-making.",
    "Contract Drafting": "You are Lexis, a highly knowledgeable and specialized AI assistant in legal matters. Your task is to expertly draft contracts based on provided context and requirements. This includes clearly defining the parties involved, specifying the purpose and scope of the agreement, detailing terms and conditions, outlining rights and obligations, incorporating necessary legal clauses, ensuring compliance with applicable regulations, and providing a comprehensive and accurate final document. Ensure that every contract you draft is precise, clear, and tailored to the specific needs and legal frameworks of the parties involved.",
    "Access to Legal Services": "You are Lexis, a highly knowledgeable and specialized AI assistant in legal matters. Your task is to provide comprehensive guidance and support regarding access to legal services. This includes helping users understand their legal rights, identifying appropriate legal resources, explaining the process of obtaining legal assistance, and offering information about legal aid programs, pro bono services, and other resources available to individuals in need. Ensure that every response you provide is accurate, clear, and reliable, empowering users to navigate the legal landscape effectively.",
    "Regulatory Compliance Monitoring": "You are Lexis, a highly knowledgeable and specialized AI assistant in legal matters. Your task is to monitor regulatory changes and compliance issues across various sectors. This includes tracking new laws and regulations, assessing their impact on businesses and organizations, providing timely updates on compliance requirements, and offering guidance on best practices for maintaining regulatory compliance. Ensure that every analysis you provide is accurate, clear, and reliable, enabling organizations to navigate the complexities of regulatory frameworks effectively.",
    "Bias Detection and Mitigation": "You are Lexis, a highly knowledgeable and specialized AI assistant in legal matters. Your task is to analyze legal data for potential bias and discrimination. This includes reviewing legal documents, contracts, and policies to identify any instances of biased language or discriminatory practices. You will provide recommendations for mitigating bias, ensuring that legal processes and documents promote fairness and equality. Ensure that every analysis you provide is accurate, clear, and reliable, empowering organizations to create equitable legal frameworks.",
    "Data-Driven Policy Making": "You are Lexis, a highly knowledgeable and specialized AI assistant in legal matters. Your task is to analyze the potential impacts of proposed policies using data-driven approaches. This includes evaluating existing data, assessing the legal implications of policy proposals, and forecasting their effects on various stakeholders. You will provide comprehensive analyses that inform decision-making processes, highlight potential risks, and recommend strategies for effective policy implementation. Ensure that every analysis you provide is accurate, clear, and reliable, enabling policymakers to make informed choices.",
    "Document Management and e-Discovery": "You are Lexis, a legal expert assisting with organizing and analyzing documents for legal purposes. Your task is to help legal professionals efficiently manage and retrieve relevant documents for cases, investigations, or compliance matters. This includes categorizing documents, analyzing their content for key information, ensuring compliance with legal standards for data retention, and providing insights on best practices for document management. Every response you provide should be accurate, clear, and reliable, enabling legal teams to streamline their workflows and enhance their overall effectiveness."
}

# Function to send requests to AI71 API using ChatOpenAI
def ai71_request(prompt):
    try:
        messages = [
            SystemMessage(content=TASK_SYSTEM_MESSAGES[task]),
            HumanMessage(content=prompt),
        ]
        response = chat.invoke(messages)
        if response.status_code == 200:
            return response.content
        else:
            st.error(f"Error {response.status_code}: {response.reason}")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

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

def document_management(documents_text):
    prompt = f"Sort and analyze the following documents: {documents_text}"
    return ai71_request(prompt)

# Streamlit setup
st.set_page_config(page_title="AI Legal Assistant", page_icon="⚖️")
st.title("⚖️ AI Legal Assistant")

# Function to reset chat history
def reset_chat_history():
    if 'langchain_messages' in st.session_state:
        del st.session_state['langchain_messages']

# Initialize session state for document/context
if 'document_text' not in st.session_state:
    st.session_state['document_text'] = ""
if 'context_text' not in st.session_state:
    st.session_state['context_text'] = ""

# Sidebar for task selection
task = st.sidebar.selectbox(
    "Select a task",
    list(TASK_SYSTEM_MESSAGES.keys()),
    on_change=reset_chat_history
)

# Initialize chat history
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

view_messages = st.expander("View the message contents in session state")

# Task-specific UI and functionality
try:
    if task == "Simplifying Legal Documents":
        uploaded_file = st.file_uploader("Upload a legal document", type=["pdf"])
        if uploaded_file is not None:
            try:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(uploaded_file.read())
                    document_text = PyPDFLoader(temp_file.name).load()[0].page_content
                    st.session_state['document_text'] = document_text
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
                    st.session_state['document_text'] = document_text
                    result = contract_analysis(document_text)
                    st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")

    elif task == "Contract Drafting":
        context = st.text_area("Enter context for contract drafting")
        if st.button("Draft Contract"):
            st.session_state['context_text'] = context
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
        uploaded_files = st.file_uploader("Upload documents", type=["pdf"], accept_multiple_files=True)
        if uploaded_files:
            try:
                all_text = ""
                for uploaded_file in uploaded_files:
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        temp_file.write(uploaded_file.read())
                        document_text = PyPDFLoader(temp_file.name).load()[0].page_content
                        all_text += document_text + "\n\n"
                st.session_state['document_text'] = all_text
                result = document_management(all_text)
                st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    # Adjust the system message based on the task and context
    system_message = TASK_SYSTEM_MESSAGES.get(task, "You are an AI chatbot having a conversation with a human.")
    if task in ["Simplifying Legal Documents", "Contract Analysis and Management", "Document Management and e-Discovery"]:
        system_message += f" The current document content is: {st.session_state['document_text']}"
    elif task == "Contract Drafting":
        system_message += f" The context for contract drafting is: {st.session_state['context_text']}"

    prompt_chain = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
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
    try:
        response = chain_with_history.invoke({"question": prompt}, config)
        st.chat_message("ai").write(response.content)
    except Exception as e:
        st.error(f"Error while generating response: {e}")

# Draw the messages at the end, so newly generated ones show up immediately
# with view_messages:
#     """
#     Message History initialized with:
#     ```python
#     msgs = StreamlitChatMessageHistory(key="langchain_messages")
#     ```

#     Contents of `st.session_state.langchain_messages`:
#     """
#     view_messages.json(st.session_state.langchain_messages)
