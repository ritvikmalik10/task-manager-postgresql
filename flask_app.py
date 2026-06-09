from flask import Flask, render_template, request, url_for, redirect, flash
import psycopg2
app = Flask(__name__)
app.secret_key = "taskmanager123"
conn = psycopg2.connect(
    host="localhost",
    database="taskmanager",
    user="postgres",
    password="dataanalyst",
    port="5432"
)

cursor = conn.cursor()

@app.route("/")
def home():

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'Completed'"
    )
    completed_tasks = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'Pending'"
    )
    pending_tasks = cursor.fetchone()[0]

    return render_template(
        "index.html",
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks
    )

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/tasks")
def tasks():

    cursor.execute(
        "SELECT * FROM tasks"
    )

    records = cursor.fetchall()

    return render_template(
    "tasks.html",
    tasks=records
)
@app.route("/delete/<int:task_id>")
def delete_task(task_id):

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    conn.commit()
    flash("Task deleted successfully!", "danger")
    return redirect("/tasks")

@app.route("/complete/<int:task_id>")
def complete_task(task_id):

    cursor.execute(
        """
        UPDATE tasks
        SET status = 'Completed'
        WHERE id = %s
        """,
        (task_id,)
    )

    conn.commit()
    flash("Task marked completed!", "success")

    return redirect("/tasks")

@app.route("/add", methods=["GET", "POST"])
def add_task():

    if request.method == "POST":

        task_name = request.form["task_name"]

        cursor.execute(
            """
            INSERT INTO tasks (task_name)
            VALUES (%s)
            """,
            (task_name,)
        )

        conn.commit()
        flash("Task added successfully!", "success")
        return redirect("/tasks")

    return render_template("add_task.html")
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):

    if request.method == "POST":

        new_task = request.form["task_name"]

        cursor.execute(
            """
            UPDATE tasks
            SET task_name = %s
            WHERE id = %s
            """,
            (new_task, task_id)
        )

        conn.commit()

        flash("Task updated successfully!", "success")

        return redirect("/tasks")

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    task = cursor.fetchone()

    return render_template(
        "edit_task.html",
        task=task
    )

app.run(debug=True)