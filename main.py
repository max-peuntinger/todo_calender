from typing import List, Dict
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template
from datetime import datetime, timedelta

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Dictionary to store tasks with dates as keys
tasks: Dict[str, List[str]] = {}

def get_next_week_dates():
    today = datetime.today()
    return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

@app.get("/", response_class=HTMLResponse)
async def read_root():
    week_dates = get_next_week_dates()
    with open("templates/index.html") as f:
        template = Template(f.read())
    return HTMLResponse(content=template.render(tasks=tasks, week_dates=week_dates), status_code=200)

@app.post("/add", response_class=HTMLResponse)
async def add_task(task: str = Form(...), task_date: str = Form(...)):
    if task_date not in tasks:
        tasks[task_date] = []
    tasks[task_date].append(task)
    week_dates = get_next_week_dates()
    with open("templates/todo_list.html") as f:
        template = Template(f.read())
    return HTMLResponse(content=template.render(tasks=tasks, week_dates=week_dates), status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
