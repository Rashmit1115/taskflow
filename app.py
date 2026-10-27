
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "tasks.db"


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                status TEXT NOT NULL DEFAULT 'To Do'
            )
        """)


@app.route("/")
def index():
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        tasks = conn.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if title:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute(
                "INSERT INTO tasks (title, description) VALUES (?, ?)",
                (title, description)
            )

    return redirect(url_for("index"))


@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    status = request.form.get("status", "To Do")
    allowed_statuses = ["To Do", "In Progress", "Done"]

    if status in allowed_statuses:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute(
                "UPDATE tasks SET status = ? WHERE id = ?",
                (status, task_id)
            )

    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return redirect(url_for("index"))


init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
