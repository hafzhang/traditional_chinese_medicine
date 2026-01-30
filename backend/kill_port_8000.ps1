# Kill all processes listening on port 8000
$pids = Get-NetTCPConnection -LocalPort 8000 -State Listen | Select-Object -ExpandProperty OwningProcess
foreach ($pid in $pids) {
    Write-Host "Killing process $pid"
    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
}
Write-Host "Killed $($pids.Count) processes"
