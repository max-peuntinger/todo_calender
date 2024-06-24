from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template
from datetime import datetime, timedelta
import sqlite3

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db_connection():
    conn = sqlite3.connect('todo_calendar.db')
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def get_next_week_dates():
    today = datetime.today()
    return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()
    conn.close()
    
    tasks = {}
    for row in rows:
        task_date = row['task_date']
        if task_date not in tasks:
            tasks[task_date] = []
        tasks[task_date].append({'id': row['id'], 'task': row['task'], 'done': row['done']})
    return tasks

@app.get("/", response_class=HTMLResponse)
async def read_root():
    week_dates = get_next_week_dates()
    tasks = get_tasks()
    with open("templates/index.html") as f:
        template = Template(f.read())
    return HTMLResponse(content=template.render(tasks=tasks, week_dates=week_dates), status_code=200)

@app.post("/add", response_class=JSONResponse)
async def add_task(task: str = Form(...), task_date: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (task, task_date) VALUES (?, ?)', (task, task_date))
    conn.commit()
    conn.close()
    
    return JSONResponse(content={'success': True})

@app.post("/update_task_status", response_class=JSONResponse)
async def update_task_status(request: Request):
    data = await request.json()
    task_id = data.get('task_id')
    done = data.get('done')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET done = ? WHERE id = ?', (done, task_id))
    conn.commit()
    conn.close()
    
    return JSONResponse(content={'success': True})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
