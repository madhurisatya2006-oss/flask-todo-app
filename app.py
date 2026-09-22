from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    task = request.form["task"]

    conn = get_db()
    conn.execute("INSERT INTO tasks (task, completed) VALUES (?, ?)",
                 (task, 0))
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/complete/<int:id>")
def complete_task(id):
    conn = get_db()
    conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete_task(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")


def create_database():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    app.run(debug=True)