# Verify compression results
$sourceDir = $PSScriptRoot
$targetSizeKB = 200

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Compression Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$jpgFiles = Get-ChildItem -Path $sourceDir -Filter *.jpg -File
$totalFiles = $jpgFiles.Count
$overTarget = 0
$totalSize = 0

foreach ($file in $jpgFiles) {
    $totalSize += $file.Length
    if ($file.Length -gt $targetSizeKB * 1024) {
        $overTarget++
        $sizeKB = [math]::Round($file.Length / 1KB, 2)
        Write-Host "OVER TARGET: $($file.Name) - $sizeKB KB" -ForegroundColor Red
    }
}

$totalSizeMB = [math]::Round($totalSize / 1MB, 2)
$avgSizeKB = [math]::Round($totalSize / $totalFiles / 1KB, 2)

Write-Host ""
Write-Host "Total files: $totalFiles" -ForegroundColor White
Write-Host "Files over 200KB: $overTarget" -ForegroundColor $(if ($overTarget -eq 0) { "Green" } else { "Red" })
Write-Host "Total size: $totalSizeMB MB" -ForegroundColor Cyan
Write-Host "Average file size: $avgSizeKB KB" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($overTarget -eq 0) {
    Write-Host "SUCCESS: All files are under 200KB!" -ForegroundColor Green
} else {
    Write-Host "WARNING: $overTarget files are still over 200KB" -ForegroundColor Red
}
Write-Host "========================================" -ForegroundColor Cyan
