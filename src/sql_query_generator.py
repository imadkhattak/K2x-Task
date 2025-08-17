import os
import ollama

def get_schema_path():
    return os.path.join(os.path.dirname(__file__), "database_schema.txt")

def get_sql_prompt(user_question: str) -> str:
    schema_path = get_schema_path()
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = f.read()

    return f"""Generate a MySQL SELECT query based on this database schema:
{schema}

Rules:
1. Generate ONLY READ queries (SELECT, no INSERT/UPDATE/DELETE)
2. Use WHERE for filtering when needed
3. Return ONLY the raw SQL query — no explanations, no markdown, no backticks, no quotes
4. Include JOINs if needed based on the schema
5. Use proper table aliases when joining tables
6. Never modify the database (only read operations)
7. Always start the query with SELECT

Question: "{user_question}"
SQL:"""

def generate_sql(question: str) -> str:
    prompt = get_sql_prompt(question)
    response = ollama.generate(
        model="llama3:8b",
        prompt=prompt,
        options={"temperature": 0.1}
    )
    return response["response"].strip()
