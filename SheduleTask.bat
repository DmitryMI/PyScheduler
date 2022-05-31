@echo off

set /P timeout="Timeout in minutes: "

set /P command="Command: "

python PyScheduler/PyScheduler.py --delay %timeout% --name PyScheduler\DisplaySleepTask --command "%command%"

pause