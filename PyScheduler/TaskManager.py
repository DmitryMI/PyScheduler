from datetime import datetime
import subprocess

CREATE_TASK_OK = 0

PERIOD_ONCE = "ONCE"

def print_array(arr):
    message = ""
    for item in arr:
        message = message + item + " "
    print(message)

def create_task(task_name, period, command, start_time: datetime, self_destuct_enabled=False):
    # SCHTASKS /CREATE /SC ONCE /TN "PyScheduler\DebugTask" /TR "C:\Users\DmitriyBigPC\Documents\GitHub\PyScheduler\script_example.bat" /ST 15:45

    shell_sc = period 
    #shell_tn = f"\"{task_name}\""
    shell_tn = task_name
    #shell_tr = f"\"{command}\""
    shell_tr = command
    shell_st = start_time.strftime("%H:%M")

    shell = ["SCHTASKS", "/CREATE", "/SC", shell_sc, "/TN", shell_tn, "/TR", shell_tr, "/ST", shell_st]

    if self_destuct_enabled:
        shell.append("/Z")

    print_array(shell)

    process = subprocess.Popen(shell, 
                           stdout=subprocess.PIPE,
                           universal_newlines=True
                           )
    while True:
        output = process.stdout.readline()

        return_code = process.poll()
        if return_code is not None:
            print('CREATE TASK RETURN CODE:', return_code)
            break

    if(return_code != 0):
        return return_code

    return 0


def delete_task(task_name):
    # SCHTASKS /DELETE /TN "PyScheduler\DebugTask" /F
    #shell_tn = f"\"{task_name}\""
    shell_tn = task_name
    shell = ["SCHTASKS", "/DELETE", "/TN", shell_tn, "/F"]
    print_array(shell)

    process = subprocess.Popen(shell, 
                           stdout=subprocess.PIPE,
                           universal_newlines=True
                           )
    while True:
        output = process.stdout.readline()

        return_code = process.poll()
        if return_code is not None:
            print('DELETE_TASK RETURN CODE:', return_code)
            break

    if(return_code != 0):
        return return_code

    return 0
