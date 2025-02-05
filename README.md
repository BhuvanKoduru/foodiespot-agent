# sarvam-assignment

# FoodieSpot AI Agent

- This project enables an AI-driven restaurant reservation system. Follow the steps below to set up and run the project.
- [Notion link](https://www.notion.so/Creating-a-Restaurant-Reservation-Bot-19131cf78e8180e0a169c6727b9a72b0?pvs=4)
- Please mail me (bckoduru@gmail.com) if you are unable to access the site.
## Prerequisites

Make sure you have the following installed:

- **Python 3.x**: For running the Python scripts.
- **Ollama**: For running the language model server. You can install Ollama from [here](https://ollama.com).
- **Streamlit**: For running the web application.

## Setup Instructions

### 1. Set up the Database

Run the following command to initialize the database and populate the tables with sample data:

- python db.py
- This will create the necessary tables and insert sample data into your SQLite database.

2. Start Ollama Server
Start the Ollama server by running the following command in the terminal:

- ollama run
- Ensure that Ollama is installed and running properly before proceeding. You can check its installation guide for troubleshooting if needed.

3. Run the Streamlit App
Once Ollama is running, start the Streamlit app by running:

- streamlit run app.py
- This will start a local server and open the app in your browser, where you can interact with the FoodieSpot AI Agent.

Troubleshooting
If you encounter any issues while starting the Ollama server or running the app, make sure you have installed all necessary dependencies, and check the respective documentation for Ollama and Streamlit.
Ensure that the database was successfully populated by running python db.py before starting the app.
