@echo off

REM Set the directory path and file names
set "user=Rafael"
set "directory=C:\Users\%user%\AppData\Local\Temp"
set "file1=hammerdb_output.log"
set "file2=hdbtcount.log"
set "file3=hdbxtprofile.log"
set "file4=hammermetrics.csv"
set "file5=hservermetrics.csv"


REM Change to the target directory
cd /d "%directory%"
if errorlevel 1 (
    echo Directory does not exist: %directory%
    exit /b 1
)

REM Check if each file exists and delete it if it does
for %%f in ("%file1%" "%file2%" "%file3%" "%file4%" "%file5%") do (
    if exist "%%f" (
        del "%%f"
        echo Deleted %%f
    )
)

REM Change to HammerDB directory
cd "C:\Program Files\HammerDB-4.10"

REM Start hammerdbcli.bat in the background and get its process ID
start "" hammerdbcli.bat auto "C:\Users\%user%\Desktop\test.tcl" > "C:\Users\%user%\AppData\Local\Temp\%file1%" 2>&1

REM Add 2 seconds of wait to let the process be created
timeout /T 2 /NOBREAK >NUL

REM Get the process ID of tclsh86t
for /f "tokens=2" %%A in ('tasklist /FI "IMAGENAME eq tclsh86t.exe" /NH') do (
    set "PID=%%A"
    echo Found HammerDB PID: %%A
)

REM Get the PID of the postgres service
for /f "tokens=3" %%a in ('sc queryex "postgresql-x64-16" ^| find "PID"') do (
    set "postgres_pid=%%a"
    echo Found PostgreSQL PID: %%A
)

REM Create marker files for both monitoring scripts
echo. > "%directory%\monitor_%PID%.stop"
echo. > "%directory%\monitor_%postgres_pid%.stop"

REM Start the monitoring script for HammerDB
powershell -ExecutionPolicy Bypass -File "C:\Users\%user%\Desktop\monitor_script.ps1" -ProcessID %PID% -OutputFileName "hammermetrics.csv" -StopFile "%directory%\monitor_%PID%.stop"

REM Start the monitoring script for PostgreSQL
powershell -ExecutionPolicy Bypass -File "C:\Users\%user%\Desktop\monitor_script.ps1" -ProcessID 5596 -OutputFileName "hservermetrics.csv" -StopFile "%directory%\monitor_%postgres_pid%.stop"

REM Wait for tclsh86t process to stop
:wait
tasklist /FI "PID eq %PID%" 2>NUL | find /I "%PID%" >NUL
if "%ERRORLEVEL%"=="0" (
    timeout /T 5 /NOBREAK >NUL
    goto wait
)

REM Once tclsh86t process stops, delete the stop files to signal the monitoring scripts to stop
del "%directory%\monitor_%PID%.stop"
del "%directory%\monitor_%postgres_pid%.stop"

endlocal
