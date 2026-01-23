$ErrorActionPreference = "Stop"
Write-Host "Searching for reference file..."
$file = Get-ChildItem -Path "e:\a_shangzhan\traditional_chinese_medicine" -Filter "百会.jpg" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if ($file) {
    $dir = $file.DirectoryName
    Write-Host "Found source directory: $dir"
    
    $dest = "e:\a_shangzhan\traditional_chinese_medicine\backend\static\acupoints"
    if (-not (Test-Path $dest)) {
        New-Item -ItemType Directory -Path $dest
    }
    
    Write-Host "Copying files to $dest..."
    Copy-Item "$dir\*.jpg" -Destination $dest -Force
    
    Write-Host "Copy complete."
} else {
    Write-Host "Could not find reference file '百会.jpg'."
}
