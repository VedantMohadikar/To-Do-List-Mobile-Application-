import tkinter as tk
import sqlite3
from datetime import datetime

# DATABASE SETUP 
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    priority TEXT DEFAULT 'MEDIUM',
    created_at TEXT
)
""")
conn.commit()

# FUNCTIONS 
def load_tasks():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT id, title, completed, priority FROM tasks")
    for task in cursor.fetchall():
        status = "✔ " if task[2] else ""
        display = f"{status}{task[1]}  [{task[3]}]"
        listbox.insert(tk.END, display)

def add_task():
    task = entry.get()
    priority = priority_var.get()

    if task:
        cursor.execute(
            "INSERT INTO tasks (title, completed, priority, created_at) VALUES (?, 0, ?, ?)",
            (task, priority, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        entry.delete(0, tk.END)
        load_tasks()

def mark_completed():
    selected = listbox.curselection()
    if selected:
        task_id = selected[0] + 1
        cursor.execute(
            "UPDATE tasks SET completed = 1 WHERE id = ?",
            (task_id,)
        )
        conn.commit()
        load_tasks()

def delete_task():
    selected = listbox.curselection()
    if selected:
        task_id = selected[0] + 1
        cursor.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        conn.commit()
        load_tasks()

# UI
root = tk.Tk()
root.title("To-Do List Application")
root.geometry("360x460")

entry = tk.Entry(root, width=35)
entry.pack(pady=10)

priority_var = tk.StringVar(value="MEDIUM")
priority_menu = tk.OptionMenu(root, priority_var, "LOW", "MEDIUM", "HIGH")
priority_menu.pack()

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack(pady=5)

listbox = tk.Listbox(root, width=45, height=15)
listbox.pack(pady=10)

complete_button = tk.Button(root, text="Mark Completed", command=mark_completed)
complete_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack()

load_tasks()
root.mainloop()
