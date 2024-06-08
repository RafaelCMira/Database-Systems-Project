param(
    [int]$ProcessID,
    [string]$OutputFileName
)

$user = "Rafael"
$basePath = "C:\Users\$user\AppData\Local\Temp\"

$outputFile = Join-Path -Path $basePath -ChildPath $OutputFileName
$interval = 5  # Interval in seconds

# If the file doesn't exist, create it and write the header
if (-not (Test-Path $outputFile)) {
    "Timestamp,CPU(%),Memory(MB),DiskRead(B/s),DiskWrite(B/s)" | Out-File -FilePath $outputFile
}

# Get the number of logical processors
$logicalProcessorCount = (Get-WmiObject Win32_ComputerSystem).NumberOfLogicalProcessors


while ($true) {
    try {
        $process = Get-Process -Id $ProcessID -ErrorAction Stop

        $cpuRaw = (Get-WmiObject Win32_PerfFormattedData_PerfProc_Process | Where-Object { $_.IDProcess -eq $ProcessID }).PercentProcessorTime
        $cpu = $cpuRaw / $logicalProcessorCount  # Calculate the CPU percentage per logical processor

        $memory = $process.WorkingSet64 / 1MB
        $diskRead = (Get-WmiObject Win32_PerfFormattedData_PerfDisk_LogicalDisk | Where-Object { $_.Name -eq "_Total" }).DiskReadBytesPerSec
        $diskWrite = (Get-WmiObject Win32_PerfFormattedData_PerfDisk_LogicalDisk | Where-Object { $_.Name -eq "_Total" }).DiskWriteBytesPerSec

        $timestamp = Get-Date -Format "HH:mm:ss"

        "$timestamp,$cpu,$memory,$diskRead,$diskWrite" | Out-File -FilePath $outputFile -Append
    } catch {
        # Exit the loop if the process is not found
        break
    }
    Start-Sleep -Seconds $interval
}