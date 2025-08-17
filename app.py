from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.execute_sql_query import return_sql_result
from src.get_db_schema import save_schema_to_file   # Import schema function

# Initialize FastAPI app
app = FastAPI()

# Run this once at startup (schema will always be ready before requests)
@app.on_event("startup")
async def startup_event():
    save_schema_to_file()
    print("✅ Database schema saved to src/database/schema.txt at startup")

# Mount static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 template directory
templates = Jinja2Templates(directory="templates")

# Home route -> loads index.html
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Chat API -> takes user question, generates SQL, executes it, and returns result
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
        return {
            "error": response["error"],
            "sql": response.get("sql")
        }
