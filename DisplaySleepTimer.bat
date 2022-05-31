@echo off

python PyScheduler/PyScheduler.py --clear --name PyScheduler\DisplaySleepTask

set /P timeout="State timeout in minutes: "

set /a minutes=%timeout%

python PyScheduler/PyScheduler.py --delay %minutes% --name PyScheduler\DisplaySleepTask --command %~dp0%/kill_firefox_and_display.bat

pause