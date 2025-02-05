import ollama
from ollama import ChatResponse, chat
import streamlit as st
import json
from tools import  find_alternate_restaurants, confirm_reservation,get_locations



    # Define a system message guiding Llama's behavior
SYSTEM_PROMPT = """
    You are a helpful AI assistant managing restaurant reservations for FoodieSpot. You must greet the user and be polite.
    Your role is to:
    1. Understand user intent.
    2. Call the correct tool from this list when needed:
    - `get_locations()`
    - `confirm_reservation(location, date,slot, seats_needed)`
    - `find_alternate_restaurants(date, slot, seats_needed)`
  
    
    
    You have access to the following tools:

1. **get_locations()**  
   - Use when the user asks about available restaurants. Call this when the user asks for some information about the locations available.
    get_locations() does not take any parameters. Always call it without arguments.
If the user asks for restaurants based on a cuisine, first call get_locations(), then filter the results in your response.

2. **confirm_reservation(location, date,slot, seats_needed)**  
   - Use to make a reservation. It takes the following arguments:
    1. location: Name of the restaurant
    2. Date: When the user wants to book. Either "Today" or "Tomorrow"
    3. slot: There are 4 available slots 12:00, 3:00, 6:00, 9:00
    4. seats needed: How many seats the user wants.
     DO NOT CALL THIS TOOL WITHOUT RECEIVING ALL THE PARAMETERS FROM THE USER. CONFIRM ALL THE PARAMETERS WITH THE USER BEFORE CALLING THIS.
     If this tool call is successful, let the user know! The tool message will be something like "Reservation at Waffle Wonderland has been booked on Today at time 3:00 PM for 5 people" This is a generic message.
   
3. **find_alternate_restaurants(date, slot, seats_needed)**  
   - Use if the requested restaurant is full and the user wants .
   It takes the following arguments:
    1. Date: When the user wants to book. Either "Today" or "Tomorrow"
    2. slot: There are 4 available slots 12:00, 3:00, 6:00, 9:00
    3. seats needed: How many seats the user wants.
     DO NOT CALL THIS TOOL WITHOUT RECEIVING ALL THE PARAMETERS FROM THE USER. CONFIRM ALL THE PARAMETERS WITH THE USER BEFORE CALLING THIS
   

Do not modify tool arguments. If you need to filter results, do it after receiving the tool's output and analyze it.
**If the user request is missing required details (e.g., number of people, time), ask follow-up questions to get complete information before calling a tool. Check context and previous messages for missing details.**
 **DO NOT ASSUME MISSING DETAILS. PROMPT THE USER TO GIVE THE MISSING DETAILS**
 ** ONCE YOU RECEIVE ALL THE DETAILS FOR A TOOL CALL, CONFIRM ONCE WITH THE USER.**
 **Respond naturally if no tool call is needed.**
  If no tool is needed, respond naturally to the user as the helpful asssitant you are, and prompt them for further details. 
    """
    

# Define available tools
TOOLS = {
    "get_locations": get_locations,  # Fetch all restaurant locations  # Book a table at a specific location
    "find_alternate_restaurants": find_alternate_restaurants,  # Suggest other locations
    "confirm_reservation": confirm_reservation,  # Finalize reservation
}


tools=[
 {
    'type': 'function',
    'function': {
        'name': 'get_locations',
        'description': 'Retrieve all restaurant locations. Use this to get all the locations. CALL ONLY WHEN THE USER ASKS FOR RESTAURANTS.',
        'parameters': {
            'type': 'object',
            'properties': {}  # No parameters needed
        },
    },
},
{
    'type': 'function',
    'function': {
        'name': 'find_alternate_restaurants',
        'description': 'Find alternative restaurant locations if the requested location is unavailable.',
        'parameters': {
            'type': 'object',
            'required': ['date','slot','seats_needed'],
            'properties': {
                'date': {
                    'type': 'string',
                    'description': 'The date of reservation. Either "Today" or "Tomorrow"'
                },'slot': {
                    'type': 'string',
                    'description': 'The time slot required for the reservation. There are 4 available slots 12:00, 3:00, 6:00, 9:00'
                },'seats_needed': {
                    'type': 'integer',
                    'description': 'The number of seats required for the reservation.'
                }
            },
        },
    },
},
{
    'type': 'function',
    'function': {
        'name': 'confirm_reservation',
        'description': 'Confirm and finalize a reservation after verifying availability.',
        'parameters': {
            'type': 'object',
            'required': ['location', 'date','slots','seats_needed'],
            'properties': {
                'location':
                    {
                        'type':'string',
                        'description':"The location of the restaurant"
                    },
                'date': {
                    'type': 'string',
                    'description': 'The date of reservation. Either "Today" or "Tomorrow"'
                },'slot': {
                    'type': 'string',
                    'description': 'The time slot required for the reservation. There are 4 available slots 12:00 PM, 3:00 PM, 6:00 PM, 9:00 PM'
                },'seats_needed': {
                    'type': 'integer',
                    'description': 'The number of seats required for the reservation.'
                }
            },
        },
    },
} ]


def call_tool(tool_name, arguments):
    """Dynamically call a function from TOOLS based on user intent."""
    print(f"🔧 Calling tool: {tool_name} with args {arguments}")  # Debugging

    if tool_name in TOOLS:
        result = TOOLS[tool_name](**arguments) if arguments else TOOLS[tool_name]()
        return json.dumps(result, indent=2)
    return {"error": "Invalid tool called"}
import openai
import json
import requests
def chat_with_llama():
    """Handles conversation flow and tool calling with Llama-3.1-8B."""

    api_url='http://localhost:11434/api/chat'
    payload={"model":"llama3.1:8b","messages":st.session_state['messages'],"stream":False,"tools":tools}
    # print("🔍 RAW Llama Response:", response)  # Debugging
    response_raw=requests.post(api_url,json=payload)
    response=json.loads(response_raw.text)
    print(response)
    if 'tool_calls' in response['message'].keys():
        for tool in response['message']['tool_calls']:
            function_name = tool['function']['name']
            arguments = tool['function']['arguments']

            if function_name in TOOLS:
                print(f"🔧 Calling {function_name} with {arguments}")
                output = TOOLS[function_name](**arguments)
                print("✅ Tool Output:", output)

                # Append the tool function's output first
                # st.session_state['messages'].append(response.message)

                print(response['message'])
                st.session_state['messages'].append({'role': 'tool', 'content': str(output), 'name': function_name})
        
        # Get final response with full history
        payload={"model":"llama3.1:8b","messages":st.session_state['messages'],"stream":False,"tools":tools}        
        final_response = requests.post(api_url,json=payload)
        print(st.session_state['messages'])
        response=json.loads(final_response.text)
        
        return response['message']['content']
    else:
        print("No tool call needed!")
        print(st.session_state['messages'])
        
        return response['message']['content']

