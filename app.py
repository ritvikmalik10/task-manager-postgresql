
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="taskmanager",
    user="postgres",
    password="dataanalyst",
    port="5432"
)

cursor = conn.cursor()
def view_tasks():

    cursor.execute(
        "SELECT id, task_name, status, created_at FROM tasks"
    )

    records = cursor.fetchall()

    print("\nID\tTask\t\tStatus\t\tCreated At")
    print("-" * 70)

    for row in records:
        print(f"{row[0]}\t{row[1]}\t\t{row[2]}\t\t{row[3]}")
        

def add_task():

    task_name = input("What task do you want to add: ")

    cursor.execute(
        "INSERT INTO tasks (task_name) VALUES (%s)",
        (task_name,)
    )

    conn.commit()

    print(f"Task '{task_name}' added successfully.")

def update_task():

    try:
        task_id = int(input("Enter task ID to update: "))
    except ValueError:
        print("Please enter a valid task ID.")
        return

    new_task = input("Enter new task name: ")
    

    cursor.execute(
        """
        UPDATE tasks
        SET task_name = %s
        WHERE id = %s
        """,
        (new_task, task_id)
    )

    conn.commit()

    print("Task updated successfully.")

def delete_task():

    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Please enter a valid task ID.")
        return

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    conn.commit()

    print("Task deleted successfully.")

def mark_complete():

    try:
        task_id = int(input("Enter task ID to mark as completed: "))
    except ValueError:
        print("Please enter a valid task ID.")
        return

    cursor.execute(
        """
        UPDATE tasks
        SET status = 'Completed'
        WHERE id = %s
        """,
        (task_id,)
    )

    conn.commit()

    print("Task marked as completed.")

def view_pending_tasks():

    cursor.execute(
        """
        SELECT id, task_name, status, created_at
        FROM tasks
        WHERE status = 'Pending'
        """
    )

    records = cursor.fetchall()

    print("\nPending Tasks:")
    print("-" * 70)

    for row in records:
        print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")

def view_completed_tasks():
    cursor.execute("""
        SELECT id, task_name, status, created_at
        FROM tasks
        WHERE status = 'Completed'
    """)

    records = cursor.fetchall()

    for row in records:
        print(row)

def task():
  
  print("----welcome to task management system----")

  total_tasks = int(input("Enter how many tasks you want to add "))
  for i in range (1,total_tasks+1):
    task_name = input(f"Enter task {i} = ")
    cursor.execute(
            "INSERT INTO tasks (task_name) VALUES (%s)",
            (task_name,))
    conn.commit()
task()
cursor.execute("SELECT * FROM tasks")
records = cursor.fetchall()

print("\nCurrent Tasks:")
for record in records:
    print(record)

while True:

    try:
        operation = int(input(
            "Enter 1-Add\n"
            "2-Update\n"
            "3-Delete\n"
            "4-View\n"
            "5-Mark Complete\n"
            "6-View Pending\n"
            "7-View Completed\n"
            "8-Exit\n"
        ))

    except ValueError:
        print("Please enter a valid number.")
        continue

    if operation == 1:
     add_task()


    elif operation == 2:
      update_task()
  
    elif operation == 3:
      delete_task()
       
  
    elif operation == 4:
      view_tasks()
  
  
    elif operation == 5:
     mark_complete()
  
    elif operation == 6:
     view_pending_tasks()
  
    elif operation == 7:
     view_completed_tasks()
  
  
    elif operation == 8:

     cursor.close()
     conn.close()

     print("Closing the program....")
     break 

else:
    print("input invalid")

