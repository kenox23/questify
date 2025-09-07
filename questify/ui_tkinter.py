import tkinter as tk
import database

def user_interface(root):
    root.title("Questify")
    root.geometry("300x300")

    task_frame = tk.Frame(root)
    task_frame.pack(pady=10, fill="both", expand=True)

    tasks = []

    # Function to make a GUI row for an existing task
    def create_task_row(task_id, description):
        user_input_frame = tk.Frame(task_frame)
        user_input_frame.pack(anchor="w", pady=2)

        var = tk.BooleanVar()

        def auto_delete():
            if var.get():  # if checked
                # delete from GUI
                user_input_frame.destroy()
                tasks.remove((user_input_frame, var, task_id))
                # delete from DB
                database.delete_task(task_id)

        check_button = tk.Checkbutton(user_input_frame, variable=var, command=auto_delete)
        check_button.pack(side="left")

        user_input = tk.Entry(user_input_frame, width=20)
        user_input.pack(side="left")
        user_input.insert(0, description)

        # Save edits when Enter is pressed or focus is lost
        def save_edit(event=None):
            new_text = user_input.get()
            database.update_task(task_id, new_text)

        user_input.bind("<Return>", save_edit)  # press Enter
        user_input.bind("<FocusOut>", save_edit)  # leaving the box

        tasks.append((user_input_frame, var, task_id))

    # Function to add a brand-new task
    def add_task(description="New Task"):
        task_id = database.add_task(description)  # create in DB
        create_task_row(task_id, description)    # show in GUI

    # Button to add new tasks
    add_button = tk.Button(root, text="➕", command=add_task)
    add_button.pack(pady=5)

    # Load existing tasks from DB without inserting new ones
    for task_id, description, completed in database.get_tasks():
        create_task_row(task_id, description)