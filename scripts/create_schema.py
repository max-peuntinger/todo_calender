import sqlite3

def recreate_schema():
    conn = sqlite3.connect('todo_calendar.db')
    cursor = conn.cursor()
    
    # Drop the table if it exists
    cursor.execute('DROP TABLE IF EXISTS tasks')
    
    # Create the table with the correct schema
    cursor.execute('''
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        task_date DATE NOT NULL,
        done BOOLEAN NOT NULL DEFAULT 0
    )
    ''')
    
    conn.commit()
    conn.close()

recreate_schema()
