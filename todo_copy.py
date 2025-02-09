import argparse
import json
import os

def initialize_tasks_file():
    if not os.path.exists("tasks.json"):
        with open("tasks.json", "w") as file:
            json.dump({"id": 0, "todo": [], "in-progress": [], "done": []}, file, indent=4)

def add_task(args):
    with open("tasks.json", "r+") as file:
        todo_dic = json.load(file)
        todo_dic["id"] += 1
        new_id = todo_dic["id"]
        todo_dic["todo"].append({"id": new_id, "description": args.task})
        file.seek(0)
        json.dump(todo_dic, file, indent=4)
        file.truncate()
    print("Task has been added to the list")

def update_task(args):
    with open("tasks.json", "r+") as file:
        todo_dic = json.load(file)
        task_found = False
        
        for key, category in todo_dic.items():  # Ensure only task lists are processed
            if isinstance(category, list):
                for task in category:
                    if task["id"] == args.taskid:
                        task["description"] = args.task
                        task_found = True
                        break
                if task_found:
                    break
        
        if not task_found:
            print(f"No task found with ID {args.taskid}")
            return
        
        file.seek(0)
        json.dump(todo_dic, file, indent=4)
        file.truncate()
    print("Task has been updated")

def delete_task(args):
    with open("tasks.json", "r+") as file:
        todo_dic = json.load(file)
        task_found = False
        
        for category in todo_dic.values():
            if isinstance(category, list):
                for index, task in enumerate(category):
                    if task["id"] == args.taskid:
                        category.pop(index)
                        task_found = True
                        break
                if task_found:
                    break
        
        if not task_found:
            print(f"No task found with ID {args.taskid}")
            return
        
        file.seek(0)
        json.dump(todo_dic, file, indent=4)
        file.truncate()
    print("Task has been deleted")

def list_task(args):
    with open("tasks.json", "r") as file:
        todo_dic = json.load(file)
        if args.modifier is None:
            print(json.dumps(todo_dic, indent=4))
        else:
            if args.modifier in todo_dic:
                print(json.dumps(todo_dic[args.modifier], indent=4))
            else:
                print(f"No tasks found for category: {args.modifier}")
    print("Tasks have been listed")

def mark_in_progress_task(args):
    with open("tasks.json", "r+") as file:
        todo_dic = json.load(file)
        task_found = False
        
        for index, task in enumerate(todo_dic["todo"]):
            if task["id"] == args.taskid:
                todo_dic["in-progress"].append(task)
                todo_dic["todo"].pop(index)
                task_found = True
                break
        
        if not task_found:
            print(f"No task found with ID {args.taskid}")
            return
        
        file.seek(0)
        json.dump(todo_dic, file, indent=4)
        file.truncate()
    print("Task has been marked in progress")

def mark_done_task(args):
    with open("tasks.json", "r+") as file:
        todo_dic = json.load(file)
        task_found = False
        
        for index, task in enumerate(todo_dic["in-progress"]):
            if task["id"] == args.taskid:
                todo_dic["done"].append(task)
                todo_dic["in-progress"].pop(index)
                task_found = True
                break
        
        if not task_found:
            print(f"No task found with ID {args.taskid}")
            return
        
        file.seek(0)
        json.dump(todo_dic, file, indent=4)
        file.truncate()
    print("Task has been marked done")

glbparser = argparse.ArgumentParser(prog="task-cli", description="Task CLI, made by Shekhar Chaurasiya")
subparsers = glbparser.add_subparsers(description="different features of this todo cmd")

add = subparsers.add_parser("add", description="Adds a task to the list")
add.add_argument("task", type=str, help="The task to be added to the list")
add.set_defaults(func=add_task)

update = subparsers.add_parser("update", help="Update a task")
update.add_argument("taskid", type=int, help="The id of the task to be updated")
update.add_argument("task", type=str, help="The update to be made")
update.set_defaults(func=update_task)

delete = subparsers.add_parser("delete", help="Delete a task")
delete.add_argument("taskid", type=int, help="The ID of the task to delete from the list")
delete.set_defaults(func=delete_task)

list_cmd = subparsers.add_parser("list", help="List tasks")
list_cmd.add_argument("modifier", nargs="?", type=str, help="List the task from a specific list (todo, done, in-progress)")
list_cmd.set_defaults(func=list_task)

mark_in_progress = subparsers.add_parser("mark-in-progress", help="Mark a task as in progress")
mark_in_progress.add_argument("taskid", type=int, help="The task to mark as in progress")
mark_in_progress.set_defaults(func=mark_in_progress_task)

mark_done = subparsers.add_parser("mark-done", help="Mark a task as done")
mark_done.add_argument("taskid", type=int, help="The task to mark as done")
mark_done.set_defaults(func=mark_done_task)

initialize_tasks_file()
args = glbparser.parse_args()

if hasattr(args, "func"):
    args.func(args)
else:
    glbparser.print_help()
