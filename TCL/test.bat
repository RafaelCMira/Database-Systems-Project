@echo off
cd "C:\Program Files\HammerDB-4.10"

hammerdbcli.bat auto "C:\Users\Rafael\Desktop\test.tcl" > "C:\Users\Rafael\Desktop\hammerdb_output.log" 2>&1

echo HammerDB script execution completed. See hammerdb_output.log for details.