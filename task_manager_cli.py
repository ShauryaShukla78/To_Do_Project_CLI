import datetime
from To_Do_Project_CLI.storage_txt import *
from To_Do_Project_CLI.data import tasks


# function to add task
def add_task():

    while True:
        name = input("Enter task name...").strip().title()

        if name:
            break

        print("Task name cannot be empty.")

    priority = input("Enter priority (High/Medium/Low)...").strip().capitalize()

    while priority not in ["High", "Medium", "Low"]:
        print("Invalid priority!")
        priority = input("Enter priority (High/Medium/Low)...").strip().capitalize()

    while True:
        due_date = input("Enter deadline (YYYY-MM-DD)...")

        try:
            datetime.datetime.strptime(due_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format!")

    task = {
        "task_name": name,
        "priority": priority,
        "due_date": due_date,
        "date_of_creation": str(datetime.date.today()),
        "status": "Pending"
    }

    tasks.append(task)

    save_tasks2(task)

    print("Task added successfully!")
    print("_" * 40)

def display(task):
    print(f"Name: {task['task_name']}")
    print(f"Priority: {task['priority']}")
    print(f"Status: {task['status']}")
    print(f"Due Date: {task['due_date']}")
    print(f"Created Date: {task['date_of_creation']}")

    d_date=datetime.datetime.strptime(task['due_date'], "%Y-%m-%d").date()
    cur_date=datetime.date.today()
    days_remaining=(d_date-cur_date).days

    if days_remaining >0:
        print(f"Days Left: {days_remaining} !")
    elif days_remaining==0:
        print("Due today!")
    else:
        print(f"Overdue by {abs(days_remaining)} days.")

# function to view how many tasks were added , they are pending or done ,date of creation and the deadline.
def view_tasks(): 
    global tasks
    tasks.clear() # to clear the list before loading from file, otherwise it will duplicate the tasks every time we view tasks.
    try:
        with open("tasks.txt","r") as file:
            for line in file:
                parts=line.strip().split(" | ")
                if len(parts)==5:
                    task={
                        "task_name" :parts[0],
                        "priority" :parts[1],
                        "due_date" :parts[2],
                        "date_of_creation" :parts[3],
                        "status" :parts[4],
                    }
                    tasks.append(task)
    except FileNotFoundError :
        print("No saved file found.")
        tasks.clear()
            
    if len(tasks)==0:
        print("No tasks to show...")
        return
    for ind,task in enumerate(tasks,start=1):
        print("\nTask",ind,end="\n\n")
        # for key,value in task.items():
        #     print(f"{key}:{value}")
        
        display(task)
    print("_"*40)

# function to checklist the tasks that are completed.
def complete_task():
    view_tasks()
    if len(tasks) == 0:
        print("No tasks available to complete.")
        return

    try:
        task_no = int(input("Enter task number to mark as completed: "))

        if task_no < 1 or task_no > len(tasks):
            print("Invalid task number.")
            return

        if tasks[task_no - 1]["status"] == "Done":
            print("Task is already completed.")
            return

        tasks[task_no - 1]["status"] = "Done"
        save_tasks(tasks)

        print("Task marked as completed successfully.")

    except ValueError:
        print("Please enter a valid task number.")
    except Exception as e:
        print("Error while completing task.", e)
    print("_"*40)

def delete_task():
    view_tasks()
    if len(tasks) == 0:
        print("No tasks available to delete.")
        return

    try:
        task_no = int(input("Enter task number to delete: "))

        if task_no < 1 or task_no > len(tasks):
            print("Invalid task number.")
            return

        deleted_task = tasks[task_no - 1]["task_name"]
        del tasks[task_no - 1]
        save_tasks(tasks)

        print(f"Task '{deleted_task}' deleted successfully.")

    except ValueError:
        print("Please enter a valid task number.")
    except Exception as e:
        print("Error while deleting task.", e)
    print("_"*40)


def search_task():
    view_tasks()
    if len(tasks)==0:
        print("Nothing to search...:( ")
        return
    while True:
        found=False
        count=0
        key=input("Enter keyword to search in task names  (0 to Exit)...").lower() # to make search case-insensitive
        if key == "0":
            print("Exiting search...")
            break
        for task in tasks:
            if key in task["task_name"].lower():
                count+=1
                found=True
                print("\n" + "-" * 40)
                print("Matching Task Found")
                display(task)

        if found:
            print(f"\nFound {count} task(s) matching the keyword.")
            break
        print("\nNot found!! \nTry another keyword...")
        print("-"*40)

def filter_tasks():
    if len(tasks)==0:
        print("Nothing to filter!")
        return

    try:
        while True:
            found=False
            print("\nFilter by:\n1. Priority\n2. Status\n3. Due Date\n4. Exit")

            choice=input("Enter your choice: ")

            if choice=='1':
                while True:
                    print("\n" + "-" * 40)
                    priority=input("How to filter? (High/Medium/Low/1. (for Exit)): ")
                    if priority=='1':
                        break
                    for task in tasks:
                        if priority.lower()==task["priority"].lower():
                            found=True
                            print("\n" + "-" * 40)
                            display(task)
                    if not found:
                        print("Not found with this priority! ")
                   

            elif choice=='2':
                status=input("How to filter? (Pending/Done): ")
                for task in tasks:
                    if status.lower()==task["status"].lower():
                        found=True
                        print("\n" + "-" * 40)
                        display(task)
                if not found:
                    print("Not found with this status! ")

            elif choice=='3':
                duedate=input("Enter due date to filter (YYYY-MM-DD): ")
                for task in tasks:
                    if duedate==task["due_date"]:
                        found=True
                        print("\n" + "-" * 40)
                        display(task)
                if not found:
                    print("Not found with this due date! ")

            elif choice=='4':
                print("Exiting filter menu.")
                break
        
            else:
                print("Invalid choice!")
        if not found:
            print("Nothing found matching the filter criteria!")
        print("-"*40)
    except Exception as e:
        print(e)

def edit_task():
    if len(tasks)==0:
        print("Nothing to edit!")
        return
    
    while True:
        try:
            view_tasks()
            task_num=int(input("Enter task number to edit(for Exit-> 0)..."))
            if task_num==0:
                return
            if task_num>len(tasks) or task_num<1:
                print("Exceeded (or invalid ) the number of tasks...")
                return
            
            task=tasks[task_num-1]
            print("What to edit? ")
            print('''1. Name
2. Priority
3. Due Date
4. Status
5. Exit''')
            try:
                choice =int(input("\nEnter your choice..."))
                if choice==1:
                    edittask=task
                    #title() → every word uppercase
                    Name=input("Enter new name...").strip().title()
                    edittask['task_name']=Name
                    print("Name changed.")
                    save_tasks(tasks)
                    view_tasks()
                    continue
                elif choice==2:
                    edittask=task
                    Priority=input("Enter priority (High/Medium/Low)...").strip().capitalize()

                    while Priority not in ['High','Medium','Low']:
                        print("Invalid input!")
                        Priority=input("Enter priority (High/Medium/Low): ").strip().capitalize()

                    edittask['priority']=Priority
                    print("Priority changed.")
                    save_tasks(tasks)
                    view_tasks()
                    continue
                elif choice==3:
                    edittask=task
                    while True:
                        DueDate=input("Enter new deadline (due date [YYYY-MM-DD]) for the task...")
                        try:
                            datetime.datetime.strptime(DueDate, "%Y-%m-%d") #String parse time, it converts string into date object
                            break
                        except ValueError:
                            print("Invalid format.")

                    edittask['due_date']=DueDate
                    print("Due date has been changed.")
                    save_tasks(tasks)
                    view_tasks()
                    continue
                elif choice==4:
                    edittask=task
                    Status=input("Enter new status (Done/Pending) for the task...").capitalize()

                    while Status not in ['Done','Pending']:
                        print("Invalid input!")
                        Status=input("Enter new status (Done/Pending) for the task...").capitalize()

                    edittask['status']=Status
                    save_tasks(tasks)
                    print("Status has been updated.")
                    view_tasks()
                    continue
                elif choice==5:
                    print("You exited...")
                    break
                else:
                    print("Invalid choice...Please try again...")
            except ValueError as e:
                print("Invalid input. Please enter a number.",e)
        except ValueError as e:
            print("Invalid input. Please enter a number.",e) 
    print("_"*40)

def sort_tasks():
    view_tasks()
    if len(tasks)==0:
        print("Nothing to sort!")
        return
    #Priority sorting using mapping
    print("\nSort by: \n1.Priority \n2.Due Date \n3.Created Date \n4.Exit")
    sorting_done=False
    try:
        sort_choice=int(input("Enter your choice..."))
        if sort_choice==4:
            return
        order=input("Sorting order (asc/desc): ").strip().lower()
        while order not in ['asc','desc']:
            print("Invalid input!")
            order=input("Sorting order (asc/desc): ").strip().lower()

        if sort_choice==1:
          priority_order={"High":1,"Medium":2,"Low":3}
          tasks.sort(key=lambda task:priority_order[task["priority"]],reverse=(order=='desc'))
          sorting_done=True
          display_all_tasks()
        elif sort_choice==2:
            tasks.sort(key=lambda task:task["due_date"],reverse=(order=='desc'))
            display_all_tasks()
            sorting_done=True
        elif sort_choice==3:
            tasks.sort(key=lambda task:task["date_of_creation"],reverse=(order=='desc'))
            display_all_tasks()
            sorting_done=True
        else:
            print("Invalid choice! ")
    except (ValueError,EOFError) as e:
        print("Invalid input.", e)
    try:
        if sorting_done:
            save_choice=input("Do you want to save sorted order? (y/n): ").strip().lower()
            while save_choice not in ['y','n']:
                print("Invalid input!")
                save_choice=input("Do you want to save sorted order? (y/n): ").strip().lower()
            if save_choice=='y':
                save_tasks(tasks)
                print("Sorted order saved successfully! ")
            if save_choice=='n':
                print("Sorted order not saved. ")
    except Exception as e:
        print("Invalid input. Please enter 'y' or 'n'.", e)
    print("_"*40)

def display_all_tasks():

    if len(tasks) == 0:
        print("No tasks to show...")
        return

    for ind, task in enumerate(tasks, start=1):
        print(f"\nTask {ind}\n")

        try:
            display(task)
        except Exception as e:
            print("Error in displaying task.", e)

    print("_" * 40)