 # ====Importing Libraries====
import datetime


 # ====Function(s)====
 # Function to validate correct date format.
def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, "%d %b %Y")
        return True
    except ValueError:
        return False
 
 
 # ====Login Section====
# Read user login details from file and store them in a dictionary.
stored_login_details = {}
with open("user.txt", "r+", encoding = "utf-8") as file:
    for line in file:
        stored_username, stored_password = line.strip().split(", ")
        stored_login_details[stored_username] = stored_password

print("***** Welcome to the Task Manager Programme *****\n")


# Prompt user to input login details.
while True:
    username = input("Please enter your username: ").lower()
    if username not in stored_login_details:
        print("\nError: Username not found. Please try again.\n")
    else:
        password = input("\nPlease enter your password: ").lower()
        if stored_login_details[username] != password:
            print("\nError: Incorrect password. Please try again.\n")
        else:
            print(f"\n***** Hello {username}, you are now logged in! *****\n")
            break


# ====Menu====
# Present menu of options to user.
while True:
    # Present the menu to the user and 
    # make sure that the user input is converted to lower case.
    if username == "admin":
        menu = input('''Select one of the following options:
        r - register a user
        a - add task
        va - view all tasks
        vm - view my tasks
        ut - update tasks
        ds - display statistics
        e - exit
        : ''').lower()
    elif username != "admin":
        menu = input('''Select one of the following options:
        a - add task
        va - view all tasks
        vm - view my tasks
        ut - update tasks
        e - exit
        : ''').lower()


    # ====Register a User====
    # Only 'admin' has the ability to register a user.
    if menu == 'r':
        if username == "admin":
            while True:
                new_username = input("\nPlease enter a new username: ").lower()
                if new_username not in stored_login_details:
                    break
                else:
                    print("\nError: Username already exists! Please try again.")
            new_password = input("\nPlease enter a new password: ").lower()
            new_password_confirm = input("\nPlease re-enter new password: ").lower()
            if new_password_confirm == new_password:
                with open("user.txt", "a+", encoding = "utf-8") as file:
                    file.write(f"\n{new_username}, {new_password}")
                    print("\n***** New username and password have been added! *****\n")
                stored_login_details[new_username] = new_password
            else:
                print("\nError: Passwords do not match. Please try again!\n")
        else:
            print("\nError: Only 'admin' is allowed to register new users!\n")


    # ====Add a Task====
    elif menu == 'a':
        while True:
            task_username = input("\nPlease enter username of the user you want to assign a task to: ").lower()
            if task_username not in stored_login_details:
                print("\nError: Username does not exist! Please create user before assigning a task.")
            else:
                break
        task_title = input("\nPlease enter the title of the task: ")
        task_description = input("\nPlease provide a short description of the task: ")
        while True:
            current_date = input("\nPlease provide the current date [dd Mon yyyy]: ")
            if validate_date(current_date):
                break
            else:
                print("\nError: invalid date format. Please enter date in 'dd Mon yyyy' format.")
        while True:
            task_due_date = input("\nPlease provide due date [dd Mon yyyy] for the given task: ")
            if validate_date(task_due_date):
                break
            else:
                print("\nError: invalid date format. Please enter date in 'dd Mon yyyy' format.")
        with open("tasks.txt", "a+", encoding = "utf-8") as file:
            file.write(f"\n{task_username}, {task_title}, {task_description}, {task_due_date}, {current_date}, No")
            print("\n***** New task has been added! *****\n")


    # ====View All Tasks====
    elif menu == 'va':
        with open("tasks.txt", "r+", encoding = "utf-8") as file:
            for line in file:
                task_components = line.strip().split(", ")
                print(f"\nTask:                   {task_components[1]}")
                print(f"Assigned to:            {task_components[0]}")
                print(f"Date assigned:          {task_components[3]}")
                print(f"Due date:               {task_components[4]}")
                print(f"Task Complete?          {task_components[5]}")
                print(f"Task description:       \n\t{task_components[2]}")
                print("______________________________________________________________________")
        print("\n***** All tasks have been displayed! *****\n")


    # ====View My Tasks====
    elif menu == 'vm':
        tasks_found = False
        with open("tasks.txt", "r+", encoding = "utf-8") as file:
            for line in file:
                task_components = line.strip().split(", ")
                if username == task_components[0]:
                    tasks_found = True
                    print(f"\nTask:                   {task_components[1]}")
                    print(f"Assigned to:            {task_components[0]}")
                    print(f"Date assigned:          {task_components[3]}")
                    print(f"Due date:               {task_components[4]}")
                    print(f"Task Complete?          {task_components[5]}")
                    print(f"Task description:       \n\t{task_components[2]}")
                    print("______________________________________________________________________")   
        if not tasks_found:
            print("\nYou have no tasks at the moment - Lucky you!!")
        else:
            print("\n***** All your available tasks have been displayed! *****\n")

    
    # ====Update Tasks====
    elif menu == 'ut':
        # Display available tasks for user to chose from.
        with open("tasks.txt", "r", encoding = "utf-8") as file:
            print("\n***** Available Tasks to Update *****\n")
            task_found = False
            for line in file:
                task_components = line.strip().split(", ")
                print(f"Task title: {task_components[1]}")
        update_task = input("\nPlease enter the title of the task you'd like to update: ")

        
        # Read content, update task, and rewrite 'tasks' file.
        with open("tasks.txt", "r+", encoding = "utf-8") as file:
            task_lines = file.readlines()
            file.seek(0)
            for i, line in enumerate(task_lines):
                task_components = line.strip().split(", ")
                if task_components[1] == update_task:
                    task_components[5] = "Yes"
                    task_lines[i] = ", ".join(task_components) + "\n"
                    task_found = True
        if not task_found:
            print(f"\nError: Task '{update_task}' not found. Please try again.\n")
        else:
            with open("tasks.txt", "w", encoding = "utf-8") as file:
                file.writelines(task_lines)
            print("\n***** Task successfully marked as completed! *****\n")


    # ====Display Statistics====
    # Only 'admin' has the ability to display statistics.
    elif menu == 'ds':
        if username == "admin":
            task_count = 0
            user_count = 0
            with open("tasks.txt", "r+", encoding = "utf-8") as file:
                for line in file:
                    task_components = line.strip().split(", ")
                    task_count = task_count + 1
            with open("user.txt", "r+", encoding = "utf-8") as file:
                for line in file:
                    stored_username, stored_password = line.strip().split(", ")
                    user_count = user_count + 1
            print("\n***** Task Manager - Statistics *****")
            print(f"\nThe total number of tasks are: {task_count}.")
            print(f"The total number of users are: {user_count}.")
            print("______________________________________________________________________\n")
        else:
            print("\nError: Only 'admin' is allowed to display statistics!\n")

    
    # ====Exit====
    elif menu == 'e':
        print(f'\nGoodbye, {username}!!')
        exit()


    # ====Error Handling====
    else:
        print("\nYou have entered an invalid input. Please try again!\n")