# JPG Image Compression Script
Add-Type -AssemblyName System.Drawing

$targetSizeKB = 200
$sourceDir = "C:\Users\Administrator\Documents\claude过滤蔬菜图"

$jpgFiles = Get-ChildItem -Path $sourceDir -Filter *.jpg -File
$totalFiles = $jpgFiles.Count
$filesNeedCompression = 0
$filesCompressed = 0
$filesSkipped = 0
$totalOriginalSize = 0
$totalCompressedSize = 0

Write-Host "Starting compression task..." -ForegroundColor Cyan
Write-Host "Total files found: $totalFiles" -ForegroundColor Yellow
Write-Host "Target size: 200 KB" -ForegroundColor Yellow
Write-Host ""

foreach ($file in $jpgFiles) {
    $fileSizeKB = [math]::Round($file.Length / 1KB, 2)
    $totalOriginalSize += $file.Length

    if ($file.Length -gt $targetSizeKB * 1024) {
        $filesNeedCompression++
        Write-Host "[$filesNeedCompression] Processing: $($file.Name) - Size: $fileSizeKB KB" -ForegroundColor Yellow

        try {
            $originalImage = [System.Drawing.Image]::FromFile($file.FullName)
            $jpegCodec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq "image/jpeg" } | Select-Object -First 1
            $encoderParams = New-Object System.Drawing.Imaging.EncoderParameters(1)
            $tempFile = $file.FullName + ".temp"

            $quality = 75
            $success = $false

            for ($i = 0; $i -lt 8; $i++) {
                $q = 75 - ($i * 5)
                $encoderParams.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, $q)
                $originalImage.Save($tempFile, $jpegCodec, $encoderParams)
                $tempFileSize = (Get-Item $tempFile).Length

                if ($tempFileSize -le $targetSizeKB * 1024) {
                    $originalImage.Dispose()
                    Remove-Item $file.FullName -Force
                    Rename-Item $tempFile $file.FullName
                    $newSizeKB = [math]::Round($tempFileSize / 1KB, 2)
                    $savedPercent = [math]::Round(($file.Length - $tempFileSize) / $file.Length * 100, 1)
                    $totalCompressedSize += $tempFileSize
                    $filesCompressed++
                    Write-Host "    SUCCESS: New size $newSizeKB KB (Quality: $q, Saved: $savedPercent percent)" -ForegroundColor Green
                    $success = $true
                    break
                } else {
                    Remove-Item $tempFile -Force -ErrorAction SilentlyContinue
                }
            }

            if (-not $success) {
                $originalImage.Dispose()
                $totalCompressedSize += $file.Length
                Write-Host "    FAILED: Could not compress under target size" -ForegroundColor Red
            }
        } catch {
            $totalCompressedSize += $file.Length
            Write-Host "    ERROR: $_" -ForegroundColor Red
        }
    } else {
        $totalCompressedSize += $file.Length
        $filesSkipped++
        Write-Host "  SKIP: $($file.Name) - Size: $fileSizeKB KB (already OK)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "COMPRESSION REPORT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Total files: $totalFiles"
Write-Host "Files compressed: $filesCompressed"
Write-Host "Files skipped: $filesSkipped"
Write-Host ""
$originalMB = [math]::Round($totalOriginalSize / 1MB, 2)
$compressedMB = [math]::Round($totalCompressedSize / 1MB, 2)
$savedMB = [math]::Round(($totalOriginalSize - $totalCompressedSize) / 1MB, 2)
$savedPercent = [math]::Round(($totalOriginalSize - $totalCompressedSize) / $totalOriginalSize * 100, 1)
Write-Host "Original total size: $originalMB MB"
Write-Host "Compressed total size: $compressedMB MB"
Write-Host "Space saved: $savedMB MB ($savedPercent percent)"
Write-Host "========================================" -ForegroundColor Cyan
