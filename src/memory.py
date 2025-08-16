session_memory = {
    "history": []  
}


def get_cached_answer(question: str):

    if not session_memory["history"]:
        return None

    last_turn = session_memory["history"][-1]
    last_data = last_turn["data"]

    if not last_data:
        return None

    available_fields = set(last_data[0].keys())

    for field in available_fields:
        if field.lower() in question.lower():
            filtered = [{field: row[field]} for row in last_data]
            return {
                "success": True,
                "sql": last_turn["sql"],
                "data": filtered,
                "from_cache": True
            }

    return None


def save_to_memory(question: str, sql: str, data: list[dict]):

    session_memory["history"].append({
        "question": question,
        "sql": sql,
        "data": data
    })
