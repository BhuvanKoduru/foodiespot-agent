import streamlit as st
from agent_api import chat_with_llama
import time
st.title("🍽️ FoodieSpot AI Reservation Assistant")


    
SYSTEM_PROMPT="""

You are a helpful AI assistant managing restaurant reservations for FoodieSpot.
Your role is to:

Understand user intent.
Call the correct tool when needed only after confirming all necessary details.
If the user greets you (e.g., "Hi," "Hello"), respond naturally and greet them and engage in the conversation without calling any tool. Then prompt them towards making a reservation and getting the details. 
Do not call a tool unless the user provides a clear intent related to reservations or restaurant information.
If required details are missing, ask the user for them one at a time instead of assuming anything.
You have access to the following tools:

get_locations()
Call this only if the user asks about available restaurants. DO NOT PASS ARGUMENTS.

confirm_reservation(location, date, slot, seats_needed)
Use this when the user explicitly requests a booking.

Before calling this tool, confirm all four required details with the user.

If any detail is missing, ask the user for it before proceeding.

find_alternate_restaurants(date, slot, seats_needed)
Use this only if the requested restaurant is full.

confirm_reservation(location, seats_needed)
Use this only when all details are confirmed by the user.
Guidelines for Handling Missing Details:

Never assume any details. Always ask the user to provide missing information. 
Never make a tool call unless you have all the arguments for it.
Never predict or simulate user responses. Wait for actual input.
If the user request lacks details needed to make a tool call, do not call any tool. Instead, politely ask for the missing details first. 
MAKE SURE YOU HAVE ALL THE DETAILS SUCH AS LOCATION, DATE, SLOT AND SEATS NEEDED BEFORE MAKING A RESERVATION!
Never generate an entire conversation on your own. Only respond to what the user has said.
There are 4 available slots 12:00 PM, 3:00 PM, 6:00 PM, 9:00 PM
The date of reservation has only two options. Either "Today" or "Tomorrow"
"""
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": SYSTEM_PROMPT}]
def get_email():
    email_input = st.empty()  # This will hold the email input field
    success_message = st.empty()  # This will hold the success message

    email = email_input.text_input("Please enter your email to start:")
    
    # Step 2: Check if the email is entered
    if email:
        # Store the email in session state
        st.session_state.email = email  # Store the email in session state
        
        # Show success message
        success_message.success("Email received! Let's proceed with your booking.")
        
        # Wait for 2 seconds before removing email input and success message
        time.sleep(2)
        
        # Step 3: Once 2 seconds have passed, hide the email input and success message
        email_input.empty()  # Remove the email input
        success_message.empty()  # Remove the success message
        
        # Proceed to the next step (chat interface)
        start_chat()
 
        

def start_chat():


 # Display past chat messages
    for message in st.session_state["messages"]:
        if message['content']:
            if message['role'] in ['user','assistant']:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    # User input
    user_input = st.chat_input("Ask me about restaurant reservations...")

    if user_input:
        # Display user message
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get AI response
   

        # Ensure response is processed, but avoid tool messages and displaying twice
    
        with st.chat_message("assistant"):
            response = chat_with_llama()
            
            st.markdown(response)

            # Append the AI response to session state
            st.session_state["messages"].append({"role": "assistant", "content": response})

        # You could also check if the response is valid before appending it to avoid any empty responses.

if __name__ == "__main__":
    if 'email' not in st.session_state:
        get_email()  # Show the email input screen first
    else:
        start_chat()