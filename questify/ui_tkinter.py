import tkinter as tk
import database

def user_interface(root):
    """Initialize the main window for user interface.

    Keyword arguments:
    root -- the main Tkinter window.
    """
    
    # Set window settings
    root.title("Questify")
    root.geometry("300x300")
    icon = tk.PhotoImage(file="../images/questify-logo.png")
    root.iconphoto(True, icon)

    # Container frame for all tasks
    task_frame = tk.Frame(root, bd=2, relief="solid")
    task_frame.pack(padx=10 ,pady=10, fill="both", expand=True)

    # List to store task elements
    tasks = []

    def create_task_row(task_id, description):
        """Creates the task.

        Keyword arguments:
        task_id -- identifier for the task from the database.
        description -- task description
        """

        # Frame for individual task row
        user_input_frame = tk.Frame(task_frame)
        user_input_frame.pack(anchor="w", pady=2)

        is_completed = tk.BooleanVar()

        def auto_delete():
            """Delete the task from window and database if check_button is checked.
            """
            
            # If bool is_completed true, destroy user_input_frame, remove from task = [], remove from database
            if is_completed.get():
                user_input_frame.destroy()
                tasks.remove((user_input_frame, is_completed, task_id))
                database.delete_task(task_id)

        # Frame for check button
        check_button = tk.Checkbutton(user_input_frame, variable=is_completed, command=auto_delete)
        check_button.pack(side="left")

        # Frame for user input
        user_input = tk.Entry(user_input_frame, width=20)
        user_input.pack(side="left")
        user_input.insert(0, description)

        def save_edit(event=None):
            """Save the current task to the database when Enter is pressed or window is exited.
            """
            new_text = user_input.get()
            database.update_task(task_id, new_text)

        user_input.bind("<Return>", save_edit)
        user_input.bind("<FocusOut>", save_edit)

        tasks.append((user_input_frame, is_completed, task_id))

    def add_task(description="New Task"):
        """Adds the task to the window and database
        
        Keyword arguments:
        description -- sets the added task to "New Task" in default.s
        """
        task_id = database.add_task(description)
        create_task_row(task_id, description)

    # Add button to window
    add_button = tk.Button(root, text="➕", command=add_task)
    add_button.pack(pady=5)

    for task_id, description, completed in database.get_tasks():
        create_task_row(task_id, description)