# Image Compression Script
# Compress all JPG files larger than 200KB

Add-Type -AssemblyName System.Drawing

# Configuration
$targetSizeKB = 200
$sourceDir = "C:\Users\Administrator\Documents\claude过滤蔬菜图"

# Statistics
$totalFiles = 0
$filesNeedCompression = 0
$filesCompressed = 0
$filesFailed = 0
$totalOriginalSize = 0
$totalCompressedSize = 0
$failedFiles = @()

# Get all JPG files
$jpgFiles = Get-ChildItem -Path $sourceDir -Filter *.jpg -File
$totalFiles = $jpgFiles.Count

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Image Compression Task Started" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Directory: $sourceDir" -ForegroundColor Yellow
Write-Host "JPG files found: $totalFiles" -ForegroundColor Yellow
Write-Host ""

# Process each file
foreach ($file in $jpgFiles) {
    $fileSizeKB = [math]::Round($file.Length / 1KB, 2)
    $totalOriginalSize += $file.Length

    if ($file.Length -gt $targetSizeKB * 1024) {
        $filesNeedCompression++
        Write-Host "[$filesNeedCompression] Processing: $($file.Name) - Original: $($fileSizeKB)KB" -ForegroundColor Yellow

        try {
            # Load original image
            $originalImage = [System.Drawing.Image]::FromFile($file.FullName)

            # Get JPEG encoder
            $jpegCodec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() |
                Where-Object { $_.MimeType -eq "image/jpeg" } |
                Select-Object -First 1

            # Create encoder parameters
            $encoderParams = New-Object System.Drawing.Imaging.EncoderParameters(1)

            # Save to temp file
            $tempFile = $file.FullName + ".temp"

            # Try different quality levels to achieve target size
            $quality = 80
            $success = $false
            $maxAttempts = 10

            for ($i = 0; $i -lt $maxAttempts; $i++) {
                # Adjust quality
                if ($i -eq 0) { $quality = 80 }
                elseif ($i -eq 1) { $quality = 75 }
                elseif ($i -eq 2) { $quality = 70 }
                elseif ($i -eq 3) { $quality = 65 }
                elseif ($i -eq 4) { $quality = 60 }
                elseif ($i -eq 5) { $quality = 55 }
                elseif ($i -eq 6) { $quality = 50 }
                elseif ($i -eq 7) { $quality = 45 }
                else { $quality = 40 }

                $encoderParams.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter(
                    [System.Drawing.Imaging.Encoder]::Quality, $quality
                )

                # Save to temp file
                $originalImage.Save($tempFile, $jpegCodec, $encoderParams)

                # Check file size
                $tempFileSize = (Get-Item $tempFile).Length

                if ($tempFileSize -le $targetSizeKB * 1024) {
                    # Success - target achieved
                    $originalImage.Dispose()
                    Remove-Item $file.FullName -Force
                    Rename-Item $tempFile $file.FullName

                    $newSizeKB = [math]::Round($tempFileSize / 1KB, 2)
                    $savedKB = [math]::Round(($file.Length - $tempFileSize) / 1KB, 2)
                    $savedPercent = [math]::Round(($file.Length - $tempFileSize) / $file.Length * 100, 1)

                    $totalCompressedSize += $tempFileSize
                    $filesCompressed++

                    $pct = "$savedPercent"
                    Write-Host "    SUCCESS: Quality=$quality%, New=$newSizeKB KB, Saved=$savedKB KB ($pct%)" -ForegroundColor Green
                    $success = $true
                    break
                } else {
                    Remove-Item $tempFile -Force -ErrorAction SilentlyContinue
                }
            }

            if (-not $success) {
                # If all attempts failed, save with last quality
                $originalImage.Save($tempFile, $jpegCodec, $encoderParams)
                $originalImage.Dispose()

                Remove-Item $file.FullName -Force
                Rename-Item $tempFile $file.FullName

                $tempFileSize = (Get-Item $file.FullName).Length
                $newSizeKB = [math]::Round($tempFileSize / 1KB, 2)
                $savedKB = [math]::Round(($file.Length - $tempFileSize) / 1KB, 2)

                $totalCompressedSize += $tempFileSize
                $filesCompressed++

                Write-Host "    PARTIAL: Quality=$quality%, New=$newSizeKB KB, Saved=$savedKB KB (above target)" -ForegroundColor Magenta
            }

        } catch {
            $filesFailed++
            $failedFiles += "$($file.Name) - $($_.Exception.Message)"
            Write-Host "    FAILED: $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        # File already under target size
        $totalCompressedSize += $file.Length
        Write-Host "  SKIP: $($file.Name) - Size: $($fileSizeKB)KB (already OK)" -ForegroundColor Gray
    }
}

# Generate report
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Compression Report" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Total files: $totalFiles" -ForegroundColor White
Write-Host "Files needed compression: $filesNeedCompression" -ForegroundColor Yellow
Write-Host "Files successfully compressed: $filesCompressed" -ForegroundColor Green
Write-Host "Files failed: $filesFailed" -ForegroundColor Red
Write-Host ""

$originalTotalMB = [math]::Round($totalOriginalSize / 1MB, 2)
$compressedTotalMB = [math]::Round($totalCompressedSize / 1MB, 2)
$savedTotalMB = [math]::Round(($totalOriginalSize - $totalCompressedSize) / 1MB, 2)
$savedTotalPercent = [math]::Round(($totalOriginalSize - $totalCompressedSize) / $totalOriginalSize * 100, 1)

Write-Host "Original total size: $originalTotalMB MB" -ForegroundColor White
Write-Host "Compressed total size: $compressedTotalMB MB" -ForegroundColor Green
$savedPct = "$savedTotalPercent"
Write-Host "Space saved: $savedTotalMB MB ($savedPct%)" -ForegroundColor Cyan
Write-Host ""

if ($filesFailed -gt 0) {
    Write-Host "Failed files:" -ForegroundColor Red
    foreach ($failedFile in $failedFiles) {
        Write-Host "  - $failedFile" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Task Completed!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
