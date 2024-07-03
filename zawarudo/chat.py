import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from config import *


class Chat:
    def __init__(self):
        pass

    # Function to get a response from the model
    def get_response(self, user_query, chat_history, place, tourist_or_local, days, date):
        # Define the template outside the function
        template = """
        User Input:

        Place: {place}
        Experience: {tourist_or_local}
        Duration: {days}
        Chatbot Response:

        Hello! I'd be delighted to help you plan an itinerary to experience {place} as a {tourist_or_local} for {days}. Here's a suggested itinerary tailored to your preferences:

        Day 1: [Customize based on place and experience]
        Morning:
        Activity/Site 1: [Description]
        Afternoon:
        Activity/Site 2: [Description]
        Evening:
        Activity/Site 3: [Description]
        Day 2: [Customize based on place and experience]
        Morning:
        Activity/Site 4: [Description]
        Afternoon:
        Activity/Site 5: [Description]
        Evening:
        Activity/Site 6: [Description]
        [Repeat as necessary for additional days]

        Tips for Visiting {place}:
        Public Transport:
        Getting Around: [Information about public transport options, ticketing, and tips]
        Etiquette:
        Local Customs: [Key etiquette tips and cultural norms to be aware of]
        Festivals:
        Events and Festivals: [Information about any local festivals or events happening during the stay duration]
        Weather around {date}:
        All Weather Bagpacker: [Weather conditions and purchases/preparations]

        Chat history:
        {chat_history}

        User question:
        {user_question}

        Details:
        {place}, {tourist_or_local}, {days}, {date}
        """

        prompt = ChatPromptTemplate.from_template(template)

        # Initialize the Hugging Face Endpoint
        llm = HuggingFaceEndpoint(
            huggingfacehub_api_token=api_token,
            repo_id=repo_id,
            task=task
        )
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({
            "chat_history": chat_history,
            "user_question": user_query,
            "place": place,
            "touristlocal": tourist_or_local,
            "days": days,
            "date": date
        })
        return response
        