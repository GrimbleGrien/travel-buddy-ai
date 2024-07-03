import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from zawarudo.chat import Chat
from zawarudo.wiki import Wiki
import datetime

# Load environment variables from .env file
# load_dotenv()

# Get the API token from environment variable
# api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
api_token = st.secrets["HUGGINGFACEHUB_API_TOKEN"]

# App config
st.set_page_config(page_title="JoJo Travels",page_icon= "🌍")
st.title("JoJo Travels ✈️")

# travel details
place = st.text_input("Which place beckons you?")
tourist_or_local = st.text_input("Do want to stand out or blend in?")
days = st.text_input("How many days (& nights)?")

today = datetime.datetime.now()
date = st.date_input(
    "Select your days of visit",
    min_value=today.date,
    format="MM.DD.YYYY",
)

# Initialize session state.
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am JoJo! How can I help you?"),
    ]
# Display chat history.
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)


# User input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    if Wiki.is_info_request(user_query):
        keywords = Wiki.extract_keywords(user_query, st.session_state.chat_history)
        response = Wiki.search_wikipedia(keywords)
    
    else:
        response = Chat.get_response(user_query, st.session_state.chat_history,place, tourist_or_local, days, date)

        # Remove any unwanted prefixes from the response
        response = response.replace("AI response:", "").replace("chat response:", "").replace("bot response:", "").strip()

        with st.chat_message("AI"):
            st.write(response)

    st.session_state.chat_history.append(AIMessage(content=response)) 