import sqlite3

# Connect to the database file
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    completed INTEGER DEFAULT 0
)
""")
conn.commit()


def add_task(description):
    cursor.execute("INSERT INTO tasks (description, completed) VALUES (?, 0)", (description,))
    conn.commit()
    return cursor.lastrowid  # always return the ID


def get_tasks():
    cursor.execute("SELECT id, description, completed FROM tasks")
    return cursor.fetchall()


def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()


def mark_completed(task_id):
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()


def close_db():
    conn.close()

def update_task(task_id, new_description):
    cursor.execute("UPDATE tasks SET description = ? WHERE id = ?", (new_description, task_id))
    conn.commit()