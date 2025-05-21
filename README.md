# Financial Advisor Chat System

This project demonstrates a chat-based interface for querying financial advisor and client information, using OpenAI's GPT models for natural language processing and FastAPI for data access.

## Project Structure

- `fa_api.py`: FastAPI service providing endpoints for financial advisor data
- `rag_demo.py`: Gradio-based chat interface for natural language queries
- `data.json`: Sample financial advisor and client data

## Setup

1. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\activate

# Activate virtual environment (Windows Command Prompt)
.\venv\Scripts\activate.bat

# Activate virtual environment (Linux/Mac)
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

## Running the Application

The application consists of two components that need to be running simultaneously:

1. Start the API server (in one terminal):
```bash
# Make sure virtual environment is activated
.\venv\Scripts\activate

# Start the API server
uvicorn fa_api:app --reload
```

2. Start the chat interface (in another terminal):
```bash
# Make sure virtual environment is activated
.\venv\Scripts\activate

# Start the chat interface
python rag_demo.py
```

## Sample Queries

Here are some example queries you can try in the chat interface:

1. List all Financial Advisors:
```
List the FA's
```
Expected response: A list of all financial advisors in the system.

2. Get clients for a specific FA:
```
Show me the clients managed by David Lee
```
Expected response: A list of all clients managed by David Lee with their basic information.

3. Get detailed client summary:
```
Show me the clients managed by David Lee & provide the summary of each clients
```
Expected response: A detailed summary of each client managed by David Lee, including:
- Client name
- Portfolio composition (stocks, mutual funds, bonds)
- Total portfolio value
- Key holdings and their values

4. Query specific holdings:
```
Show me Emily Davis's clients who hold Tesla stock
```
Expected response: Only clients managed by Emily Davis who have Tesla (TSLA) in their portfolio.

## API Endpoints

The FastAPI service provides the following endpoints:

- `GET /api/fa`: Get all financial advisor names
- `GET /api/fa/{fa_name}/clients`: Get clients for a specific financial advisor

## Features

- Natural language query processing using OpenAI's GPT models
- Real-time chat interface using Gradio
- RESTful API for data access
- Structured data handling for financial advisor information
- Precise response generation based on user queries

## Data Structure

The system uses a JSON file (`data.json`) containing information about:
- Financial Advisors (FA_NAME)
- Clients (Client_NAME)
- Holdings (Stocks, Mutual Funds, Bonds)
- Total portfolio values 