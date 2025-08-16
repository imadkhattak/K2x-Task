import ollama
from src.get_db_schema import save_schema_to_file

def get_sql_prompt(user_question: str, schema: str) -> str:

    save_schema_to_file()

    with open('src/database/schema.txt', 'r') as f:
        schema = f.read()

        """Generate prompt for LLM with schema from file"""
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
    save_schema_to_file()  
    with open('src/database/schema.txt', 'r') as f:
        schema = f.read()
    prompt = get_sql_prompt(question, schema)  
    response = ollama.generate(
        model="llama3:8b",
        prompt=prompt,
        options={"temperature": 0.1}
    )
    return response["response"].strip()