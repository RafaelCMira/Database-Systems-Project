@echo off
cd "C:\Program Files\HammerDB-4.10"

REM Start hammerdbcli.bat in the background and get its process ID
start "" hammerdbcli.bat auto "C:\Users\Rafael\Desktop\test.tcl" > "C:\Users\Rafael\AppData\Local\Temp\hammerdb_output.log" 2>&1

REM Add 2 seconds of wait to let the process be created
timeout /T 2 /NOBREAK >NUL

REM Get the process ID of tclsh86t
for /f "tokens=2" %%A in ('tasklist /FI "IMAGENAME eq tclsh86t.exe" /NH') do (
    set "PID=%%A"
    echo Found PID: %%A
)

REM Create marker files for both monitoring scripts
echo. > "C:\Users\Rafael\AppData\Local\Temp\monitor_%PID%.stop"
echo. > "C:\Users\Rafael\AppData\Local\Temp\monitor_5596.stop"

REM Start the monitoring script in PowerShell for the dynamic PID
powershell -ExecutionPolicy Bypass -File "C:\Users\Rafael\Desktop\new_monitor_script.ps1" -ProcessID %PID% -OutputFileName "hammermetrics.csv" -StopFile "C:\Users\Rafael\AppData\Local\Temp\monitor_%PID%.stop"

REM Start the monitoring script in PowerShell for the fixed PID
powershell -ExecutionPolicy Bypass -File "C:\Users\Rafael\Desktop\new_monitor_script.ps1" -ProcessID 5596 -OutputFileName "hservermetrics.csv" -StopFile "C:\Users\Rafael\AppData\Local\Temp\monitor_5596.stop"

REM Wait for tclsh86t process to stop
:wait
tasklist /FI "PID eq %PID%" 2>NUL | find /I "%PID%" >NUL
if "%ERRORLEVEL%"=="0" (
    timeout /T 5 /NOBREAK >NUL
    goto wait
)

REM Once tclsh86t process stops, delete the stop files to signal the monitoring scripts to stop
del "C:\Users\Rafael\AppData\Local\Temp\monitor_%PID%.stop"
del "C:\Users\Rafael\AppData\Local\Temp\monitor_5596.stop"

endlocal
