import os
import datetime

def clear_screen():
    # Clear the console screen
    os.system("cls" if os.name == "nt" else "clear")

def add_task(tasks):
    clear_screen()
    print("Enter 'back' at any prompt to cancel and return to the menu.\n")
    
    # Task name input
    name = input("Enter task name: ")
    if name.lower() == "back":
        print("Action canceled. Returning to menu...")
        return  # Exit the function

    # Priority input with validation
    while True:
        priority = input("Enter task priority (H - high/M - medium/L - low): ").capitalize()
        if priority.lower() == "back":
            print("Action canceled. Returning to menu...")
            return  # Exit the function
        if priority in ["H", "M", "L"]:
            break
        else:
            print("Invalid priority. Please enter 'H' - high, 'M' - medium or 'L' - low.")

    # Deadline input with validation
    while True:
        deadline = input("Enter task deadline (DD/MM/YYYY): ")
        if deadline.lower() == "back":
            print("Action canceled. Returning to menu...")
            return  # Exit the function
        try:
            datetime.datetime.strptime(deadline, "%d/%m/%Y")  # Validate deadline format
            tasks.append({"name": name, "priority": priority, "deadline": deadline, "completed": False})
            print(f"Task '{name}' added successfully.")
            break
        except ValueError:
            print("Invalid deadline format. Please use DD/MM/YYYY.")

def remove_task(tasks):
    clear_screen()
    print("Type 'back' if you wish to cancel the action.\n")
    show_tasks(tasks)

    if not tasks:
        print("No tasks to remove.")
        return

    while True:
        user_input = input("Enter the index of the task to remove (or type 'back' to cancel): ")
        if user_input.lower() == "back":
            print("\nAction canceled. Returning to the menu...")
            return

        try:
            index = int(user_input)
            if 0 <= index < len(tasks):
                removed_task = tasks.pop(index)
                print(f"\nTask '{removed_task['name']}' removed successfully.")
                break
            else:
                print("Invalid index. Please enter a valid index.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def mark_task_completed(tasks): # Mark task as completed
    # clearscreen
    clear_screen() 
    print("Type 'back' if you wish to cancel the action.\n")
    show_tasks(tasks, filter_by="pending") # Shows pending tasks

    # Check if there are pending tasks
    if not any(not task["completed"] for task in tasks):  
        print("No pending tasks to mark as complete.")
        return

    while True: # Loop until a valid index is entered
        user_input = input("Enter the index of the task to mark as completed (or type 'back' to cancel): ")
        if user_input.lower() == "back":  # Back option
            print("\nAction canceled. Returning to the menu...")
            return  # Exit the function

        try:
            index = int(user_input)
            if 0 <= index < len(tasks) and not tasks[index]["completed"]: # Check if the index is valid and task is pending
                tasks[index]["completed"] = True
                print(f"\nTask '{tasks[index]['name']}' marked as complete.")
                break  # Exit the loop after marking a task as completed
            else:
                print("Invalid index or task already completed.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def show_tasks(tasks, filter_by=None): # Shows tasks
    clear_screen() # Clear the screen
    # Filter tasks based on the filter_by parameter
    filtered_tasks = (
        [task for task in tasks if task["completed"]] if filter_by == "completed" else
        [task for task in tasks if not task["completed"]] if filter_by == "pending" else
        tasks
    ) 

    # Check if there are tasks to show
    if filtered_tasks: 
        for i, task in enumerate(filtered_tasks):
            status = "Completed" if task["completed"] else "Pending"
            print(f"[{i}] Task: {task['name']}, Priority: {task['priority']}, Deadline: {task['deadline']}, Status: {status}")
    else:
        print("No tasks to show.")

def sort_tasks_by_priority(tasks): 
    clear_screen()
    # Define priority ranking
    priority_order = {"H": 3, "M": 2, "L": 1}

    # Counting Sort Algorithm
    count = {1: [], 2: [], 3: []}  # Buckets for each priority

    # Populate the count dictionary
    for task in tasks:
        count[priority_order[task["priority"]]].append(task)

    # Gather sorted tasks from the buckets
    sorted_tasks = count[3] + count[2] + count[1]

 

    print("\nTasks sorted by priority:")
    show_tasks(sorted_tasks)

def sort_tasks_by_date(tasks): #sort task by date
    clear_screen()
    try:
        tasks.sort(key=lambda task: datetime.datetime.strptime(task["deadline"], "%d/%m/%Y")) 
        print("\nTasks sorted by date:")
        show_tasks(tasks)
    except ValueError:
        print("Error: One or more tasks have an invalid date format.")
 
def main():
    # Tasks container
    tasks = [
    ]

    menu_options = {
        "1": ("Add Task", lambda: add_task(tasks)),
        "2": ("Mark Task as Completed", lambda: mark_task_completed(tasks)),
        "3": ("Remove Task", lambda: remove_task(tasks)),
        "4": ("Show All Tasks", lambda: show_tasks(tasks)),
        "5": ("Show Pending Tasks", lambda: show_tasks(tasks, "pending")),
        "6": ("Show Completed Tasks", lambda: show_tasks(tasks, "completed")),
        "7": ("Sort Tasks by Priority", lambda: sort_tasks_by_priority(tasks)),
        "8": ("Sort Tasks by Date", lambda: sort_tasks_by_date(tasks)),
        "9": ("Exit", None)
    }

    while True:
        clear_screen()
        print("\nTo-Do List Menu:")
         # Display menu options
        for key, (desc, _) in menu_options.items():
            print(f"{key}. {desc}")

        # User input
        choice = input("Choose an option: ") 
        if choice in menu_options:
            action = menu_options[choice][1]
            if action is None:  # Exit
                print("Exiting To-Do List program. Goodbye!")
                break
            action()
            input("\nPress Enter to return to the menu...")  # Pause before returning to the menu
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

   