from itertools import zip_longest
import streamlit as st
import os
import google.generativeai as genai
from streamlit_chat import message

from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)


from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

st.set_page_config(page_title='Question Answering App')
st.header('AI Mentor')

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []  # Store AI generated responses

if 'past' not in st.session_state:
    st.session_state['past'] = []  # Store past user inputs

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""  # Store the latest user input


model = genai.GenerativeModel('gemini-1.5-flash')


def build_message_list():
    """
    Build a list of message contents including system, human, and AI messages.
    """
    # Start with the system message content
    zipped_messages = ["""You are an AI Technical Expert for Artificial Intelligence, here to guide and assist students with their AI-related questions and concerns. Please provide accurate and helpful information, and always maintain a polite and professional tone.

                1. Provide informative and relevant responses to questions about artificial intelligence,Data science, machine learning, deep learning, natural language processing, computer vision, and other related topics and fields.
                2. Avoid discussing sensitive, offensive, or harmful content. Refrain from engaging in any form of discrimination, harassment, or inappropriate behavior.
                3. If the user asks about a topic not related to AI, politely steer the conversation back to AI or inform them that the topic is outside the scope of this conversation.
                4. Be patient and considerate when responding to user queries, and provide clear explanations.
                5. If the user expresses gratitude or indicates the end of the conversation, respond with a polite farewell.
                6. Do Not generate long paragraphs in response untill unless the response is needed to be explainatory. Maximum word count should be 200.

                Remember, your primary goal is to assist and educate students in the field of Artificial Intelligence. Always prioritize their learning experience and well-being."""]
    
    # Zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append(human_msg)  # Add user messages
        if ai_msg is not None:
            zipped_messages.append(ai_msg)  # Add AI messages

    return zipped_messages

def generate_response():
    """
    Generate AI response using the model.
    """
    # Build the list of message contents
    message_list = build_message_list()

    # Generate response using the chat model
    ai_response = model.generate_content(message_list)

    return ai_response.text



# Define function to submit user input
def submit():
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt_input
    st.session_state.prompt_input = ""

#def get_gemini_response(question):
   # response = model.generate_content(question)
    #return response.text

# Create a text input for user
st.text_input('Ask your question here', key='prompt_input', on_change=submit)

if st.session_state.entered_prompt != "":
    # Get user query
    user_query = st.session_state.entered_prompt

    # Append user query to past queries
    st.session_state.past.append(user_query)

    # Generate response
    output = generate_response()

    # Append AI response to generated responses
    st.session_state.generated.append(output)


# Display the chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        # Display AI response
        message(st.session_state["generated"][i], key=str(i))
        # Display user message
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')

#input = st.text_input('input:', key='input')
#submit = st.button('Ask')

#if submit:
   # response = get_gemini_response(input)
    #st.subheader('Response:')
    #st.write(response)

