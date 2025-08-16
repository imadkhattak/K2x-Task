import sqlalchemy
from sqlalchemy import text
from src.sql_query_generator import generate_sql
from src.memory import get_cached_answer, save_to_memory


DATABASE_URL = "mysql+mysqldb://root:imad123@localhost/orgs_db"
engine = sqlalchemy.create_engine(DATABASE_URL)


def execute_sql_query(sql_query: str) -> list[dict]:
    
    with engine.connect() as conn:
        result = conn.execute(text(sql_query))
        return [dict(row._mapping) for row in result]
    

def return_sql_result(question: str) -> dict:
    try:
        # Checking caching first..
        cached = get_cached_answer(question)
        if cached:
            return cached

        sql = generate_sql(question)
        results = execute_sql_query(sql)

        save_to_memory(question, sql, results)

        return {
            "success": True,
            "sql": sql,
            "data": results,
            "from_cache": False
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "sql": sql if 'sql' in locals() else None
        }
