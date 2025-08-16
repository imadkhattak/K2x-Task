from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.execute_sql_query import return_sql_result

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")

    if not user_message:
        return JSONResponse({"error": "No message provided"}, status_code=400)

    response = return_sql_result(user_message)

    if response["success"]:
        return {
            "user": user_message,
            "sql": response["sql"],
            "data": response["data"],
            "from_cache": response.get("from_cache", False)
        }
    else:
        return {"error": response["error"], "sql": response.get("sql")}
