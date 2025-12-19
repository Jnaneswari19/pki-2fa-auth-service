# validate.ps1
# Script to validate PKI 2FA Auth Service before resubmission

Write-Host "=== Building and starting container ==="
docker compose build
docker compose up -d
Start-Sleep -Seconds 5

Write-Host "`n=== Checking container logs ==="
docker logs pki-2fa-app

Write-Host "`n=== Testing API: generate-2fa ==="
$gen = Invoke-WebRequest http://localhost:8000/generate-2fa
Write-Host $gen.Content

Write-Host "`n=== Testing API: verify-2fa (valid) ==="
$code = (ConvertFrom-Json $gen.Content).code
$bodyValid = @{ code = $code } | ConvertTo-Json -Compress
$validResp = Invoke-WebRequest -Uri http://localhost:8000/verify-2fa -Method POST -ContentType "application/json" -Body $bodyValid
Write-Host $validResp.Content

Write-Host "`n=== Testing API: verify-2fa (invalid) ==="
$bodyInvalid = @{ code = "000000" } | ConvertTo-Json -Compress
$invalidResp = Invoke-WebRequest -Uri http://localhost:8000/verify-2fa -Method POST -ContentType "application/json" -Body $bodyInvalid
Write-Host $invalidResp.Content

Write-Host "`n=== Waiting for cron job (2 minutes) ==="
Start-Sleep -Seconds 120
docker exec pki-2fa-app cat /app/data/cron.log

Write-Host "`n=== Restarting container to check persistence ==="
docker compose restart
Start-Sleep -Seconds 5
docker exec pki-2fa-app cat /app/data/seed.txt
