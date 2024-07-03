import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.retrievers import WikipediaRetriever
from config import *

class Wiki:
    def __init__(self):
        pass

    # Function to determine if a query is asking for more information on a topic
    def is_info_request(self,query):
        if "info" in query.lower():
            return True
        return False
    
    def extract_keywords(self,query,chat_history):
        template='''
        You are a travel assistant who can query wikipedia to find information on 
        destinations, public transport, hotels, weather, local customs and festivals, etc.
        Input (more info on ...): {user_question}
        Output (return searchable keywords): "keywords to search wikipedia"
        
        {chat_history}

        '''
        prompt = ChatPromptTemplate.from_template(template)

        # Initialize the Hugging Face Endpoint
        llm = HuggingFaceEndpoint(
            huggingfacehub_api_token=api_token,
            repo_id=repo_id,
            task=task
        )
        chain = prompt | llm | StrOutputParser()
        keywords = chain.invoke({
            "chat_history": chat_history,
            "user_question": query,
        })
        return keywords

    def search_wikipedia(self,keywords):
        retriever = WikipediaRetriever()
        docs = retriever.invoke(keywords)
        if docs:
            return docs[0].metadata
            # return docs[0].page_content, docs[0].metadata
        else:
            return "No information found."
