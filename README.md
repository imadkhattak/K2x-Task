
# SQL Query Generator & Executor (FastAPI + LLM)

This project is a web-based application that allows users to ask natural language questions about a MySQL database and receive SQL SELECT queries and results, powered by an LLM (Ollama/llama3) and FastAPI backend. It features schema introspection, SQL generation, query execution, and caching for efficient repeated queries.

## Features
- **Natural Language to SQL**: Converts user questions into MySQL SELECT queries using an LLM.
- **Database Schema Introspection**: Reads the schema from a live MySQL database and saves it for prompt context.
- **Query Execution**: Runs generated SQL queries and returns results as JSON.
- **Caching**: Remembers previous questions and results for faster repeated queries.
- **Web Interface**: Simple frontend using Jinja2 templates and static files.

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, MySQL, Ollama (llama3 LLM)
- **Frontend**: Jinja2, HTML, CSS, JavaScript
- **Other**: Alembic (for migrations), Python 3.9+

## Project Structure
```
├── app.py                  # FastAPI app entry point
├── src/
│   ├── db_config.py        # DB connection config
│   ├── get_db_schema.py    # Extracts DB schema
│   ├── sql_query_generator.py # LLM prompt & SQL generation
│   ├── execute_sql_query.py   # Executes SQL and handles caching
│   ├── memory.py           # In-memory cache logic
│   └── schema.txt      # Saved DB schema

├── templates/
│   └── index.html          # Main web UI
├── static/                 # JS/CSS assets
├── requirements.txt        # Python dependencies
├── alembic/                # DB migrations
```

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/imadkhattak/K2x-Task.git
cd K2x-Task
```

### 2. Create & Activate Virtual Environment
```sh
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure Database
- Edit `src/db_config.py` with your MySQL credentials and database name.
- Ensure your MySQL server is running and accessible.

### 5. Run Alembic Migrations (if needed)
```sh
alembic upgrade head
```

### 6. Start Ollama LLM Server
- Install and run Ollama (see https://ollama.com/)
- Pull the llama3 model: `ollama pull llama3:8b`
- Start the Ollama server (default: http://localhost:11434)

### 7. Launch the FastAPI App
```sh
uvicorn app:app --reload
```

### 8. Open in Browser
Go to [http://localhost:8000](http://localhost:8000) to use the app.

## Usage
- Enter a natural language question about your database (e.g., "Show all organizations created after 2023").
- The app will generate a SQL SELECT query, execute it, and display the results.
- Previous queries are cached for faster response.

## Environment Variables
- `.env` file can be used for sensitive config (not required by default).

## Requirements
- Python 3.9+
- MySQL server
- Ollama with llama3 model

## License
MIT License

## Author
- Imad khattak


