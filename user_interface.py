import tkinter as tk

def user_interface(root):
    root.title("Questify")
    root.geometry("300x300")

    task_frame = tk.Frame(root)
    task_frame.pack(pady=10, fill="both", expand=True)

    tasks = []

    # Function to create a new task row with a checkbox and text input.
    def add_task():
        user_input_frame = tk.Frame(task_frame)
        user_input_frame.pack(anchor="w", pady=2)

        var = tk.BooleanVar()

        def auto_delete():
            if var.get():  # if checked
                user_input_frame.destroy()
                tasks.remove((user_input_frame, var))

        check_button = tk.Checkbutton(user_input_frame, variable=var, command=auto_delete)
        check_button.pack(side="left")

        user_input = tk.Entry(user_input_frame, width=20)
        user_input.pack(side="left")

        tasks.append((user_input_frame, var))

    # Button that calls add_task when clicked.
    add_button = tk.Button(root, text="➕", command=add_task)
    add_button.pack(pady=5)