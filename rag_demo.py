import json
from typing import List, Dict, Any
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
import gradio as gr
import requests

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# API base URL
API_BASE_URL = "http://localhost:8000"

def get_client_details_by_fa_name(fa_name: str) -> List[Dict[str, Any]]:
    """Retrieve all client details associated with the given FA_NAME."""
    response = requests.get(f"{API_BASE_URL}/api/fa/{fa_name}/clients")
    if response.status_code == 404:
        return []
    response.raise_for_status()
    return response.json()

def get_all_fa_names() -> List[str]:
    """Return the list of all unique Financial Advisor names."""
    response = requests.get(f"{API_BASE_URL}/api/fa")
    response.raise_for_status()
    return response.json()

def process_query(query: str, history: List[List[str]]) -> str:
    """Process the natural language query using RAG and function calling."""
    
    # Define the available functions
    functions = [
        {
            "name": "get_client_details_by_fa_name",
            "description": "Retrieves all client details associated with the given FA_NAME",
            "parameters": {
                "type": "object",
                "properties": {
                    "fa_name": {
                        "type": "string",
                        "description": "The name of the Financial Advisor"
                    }
                },
                "required": ["fa_name"]
            }
        },
        {
            "name": "get_all_fa_names",
            "description": "Returns the list of all unique Financial Advisor names",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    ]

    try:
        # First, let's get the function call from the model
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that processes queries about financial advisors and their clients."},
                {"role": "user", "content": query}
            ],
            functions=functions,
            function_call="auto"
        )

        message = response.choices[0].message

        # If the model wants to call a function
        if message.function_call:
            function_name = message.function_call.name
            function_args = json.loads(message.function_call.arguments)

            # Execute the appropriate function
            if function_name == "get_client_details_by_fa_name":
                result = get_client_details_by_fa_name(function_args["fa_name"])
            elif function_name == "get_all_fa_names":
                result = get_all_fa_names()
            else:
                return "Error: Unknown function called"

            # Generate a natural language response based on the function results
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a precise and context-aware financial assistant. "
                                    "Only respond to what is explicitly asked in the user's query. "
                                    "Use the retrieved data strictly to generate a relevant and accurate summary. "
                                    "Do not include clients or details unrelated to the user's request."
                                )
                            },
                            {
                                "role": "user",
                                "content": (
                                    f"User query: \"{query}\"\n\n"
                                    f"Retrieved data (JSON): {json.dumps(result)}\n\n"
                                    "Based on the above data, please provide a natural language summary that strictly answers the user's query. "
                                    "Do not include information outside the scope of the query."
                                )
                            }
                        ]

            )
            
            return response.choices[0].message.content

        return message.content

    except Exception as e:
        return f"Error processing query: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="Financial Advisor Chat") as demo:
    gr.Markdown("# Financial Advisor Chat")
    gr.Markdown("Ask questions about financial advisors and their clients. For example:")
    gr.Markdown("- Show me the clients managed by John Smith")
    gr.Markdown("- What are all the financial advisors in the system?")
    
    chatbot = gr.Chatbot(height=600)
    msg = gr.Textbox(label="Your Question")
    clear = gr.Button("Clear")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        user_message = history[-1][0]
        bot_message = process_query(user_message, history)
        history[-1][1] = bot_message
        return history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch() 