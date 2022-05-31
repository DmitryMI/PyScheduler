import argparse
import os
import sys
from time import sleep
import xml.etree.cElementTree as ET
from datetime import datetime, timedelta
from TaskQuery import TaskQuery, TASK_QUERY_OK
from TaskManager import create_task, delete_task, PERIOD_ONCE, CREATE_TASK_OK
from TaskRepository import TaskRepository

parser = argparse.ArgumentParser(description='Schedules custom shell command with Windows Task Scheduler')

parser.add_argument('--delay',
                   dest='delay', 
                   default=60,
                   type=int, 
                   help='Delay in minutes for the command execution'
                   )

parser.add_argument('--execute',
                   dest='execute',
                   action='store_true',
                   default=False,
                   help='Execute scheduled action immediately'
                   )

parser.add_argument('--clear',
                   dest='clear',
                   action='store_true',
                   default=False,
                   help='Delete all tasks'
                   )

parser.add_argument('--name',
                   type=str,
                   dest='name',
                   help='Task name'
                   )

parser.add_argument('--command',
                   type=str,
                   help='The command to be scheduled or name of command to be executed'
                   )

args = parser.parse_args()

if args.clear and args.name is None:
    print("Clearing all existing tasks...")

    print("Deleting repository...")
    if os.path.exists(TaskRepository.get_repository_absolute_location()):
        os.remove(TaskRepository.get_repository_absolute_location())

    query = TaskQuery()
    query.read_csv()
    tasks = query.get_tasks_from_dir("PyScheduler")

    for task in tasks:
        print(f"Deleting {task} from Task Scheduler...")
        delete_task(task.name)

if args.clear and args.name is not None:
    print(f"Clearing task {args.name}...")

    print("Deleting from Task Scheduler...")
    delete_task(args.name)    
    
    print("Deleting from repository...")
    task_repository = TaskRepository(TaskRepository.get_repository_absolute_location())
    task_repository.remove_task(args.name)
   

if args.command is not None: 
    task_name = args.name
    task_repository = TaskRepository(TaskRepository.get_repository_absolute_location())    
    if task_name is None:
        task_name = task_repository.generate_name("PyScheduler\\Task_")

    print(f"Scheduling {args.command} with delay {args.delay} and name {task_name}")
    
    task_command = args.command
    
    repository_updated = task_repository.add_task(task_name, task_command)
    if not repository_updated:
        print("Failed to update repository. Probably task with this name already exists.")
        quit()

    datetime_now = datetime.now()
    datetime_now = datetime_now + timedelta(minutes=args.delay)

    path_self = os.path.realpath(__file__)
    scheduler_cmd = f"python {path_self} --execute --name {task_name}"

    result = create_task(task_name, PERIOD_ONCE, scheduler_cmd, datetime_now)
    if result != CREATE_TASK_OK:
        print("Fail")
    else:
        print("Task scheduled successfully")

if args.execute and args.name is not None:
    try:
        path_self = os.path.realpath(__file__)
        folder_self = os.path.dirname(path_self)
        os.chdir(folder_self)

        print(f"Executing task {args.name}! Cwd: {os.getcwd()}")

        task_repository = TaskRepository(TaskRepository.get_repository_absolute_location())
        command = task_repository.get_task_command(args.name)

        delete_task(args.name)
        
        task_repository.remove_task(args.name)

        print(f"Invoking {command}")
        os.system(command)

    except Exception as err:
        print(err)
        sleep(5)

    print("Exiting in 5 seconds. You can close the window manually...")
    sleep(5)
