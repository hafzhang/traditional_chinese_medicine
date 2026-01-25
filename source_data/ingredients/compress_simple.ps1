# JPG Image Compression Script
Add-Type -AssemblyName System.Drawing

 = 200
 = ''C:\Users\Administrator\Documents\claude过滤蔬菜图''

 = Get-ChildItem -Path  -Filter *.jpg -File
 = .Count
 = 0
 = 0
 = 0
 = 0
 = 0

Write-Host ''Starting compression...'' -ForegroundColor Cyan
Write-Host ''Total files: '' +  -ForegroundColor Yellow
Write-Host '' ''

foreach ( in ) {
     = [math]::Round(.Length / 1KB, 2)
     += .Length
    
    if (.Length -gt  * 1024) {
        ++
        Write-Host "[] Processing:  -  KB" -ForegroundColor Yellow
        
        try {
             = [System.Drawing.Image]::FromFile(.FullName)
             = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { C:\Users\Administrator\Documents\claude过滤蔬菜图.MimeType -eq ''image/jpeg'' } | Select-Object -First 1
             = New-Object System.Drawing.Imaging.EncoderParameters(1)
             = .FullName + ''.temp''
            
             = 75
             = 
            
            for ( = 0;  -lt 8; ++) {
                 = 75 - ( * 5)
                .Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, )
                .Save(, , )
                 = (Get-Item ).Length
                
                if ( -le  * 1024) {
                    .Dispose()
                    Remove-Item .FullName -Force
                    Rename-Item  .FullName
                     = [math]::Round( / 1KB, 2)
                     = [math]::Round((.Length - ) / .Length * 100, 1)
                     += 
                    ++
                    Write-Host "    Success:  KB (quality: , saved: %)" -ForegroundColor Green
                     = 
                    break
                } else {
                    Remove-Item  -Force -ErrorAction SilentlyContinue
                }
            }
            
            if (-not ) {
                .Dispose()
                 += .Length
                Write-Host "    Failed to compress under target" -ForegroundColor Red
            }
        } catch {
             += .Length
            Write-Host "    Error: C:\Users\Administrator\Documents\claude过滤蔬菜图" -ForegroundColor Red
        }
    } else {
         += .Length
        ++
        Write-Host "  Skip:  -  KB" -ForegroundColor Gray
    }
}

Write-Host ''''
Write-Host ''=== REPORT ==='' -ForegroundColor Cyan
Write-Host "Total files: "
Write-Host "Compressed: "
Write-Host "Skipped: "
 = [math]::Round( / 1MB, 2)
 = [math]::Round( / 1MB, 2)
 = [math]::Round(( - ) / 1MB, 2)
 = [math]::Round(( - ) /  * 100, 1)
Write-Host "Original:  MB"
Write-Host "Compressed:  MB"
Write-Host "Saved:  MB (%)"