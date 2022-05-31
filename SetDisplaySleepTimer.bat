@echo off

python PyScheduler/PyScheduler.py --clear --name PyScheduler\DisplaySleepTask

set /P timeout="State timeout in minutes: "

python PyScheduler/PyScheduler.py --delay %timeout% --name PyScheduler\DisplaySleepTask --command "%~dp0%/kill_firefox_and_display.bat 120"

pause