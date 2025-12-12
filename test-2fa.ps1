# Step 1: Generate a fresh ciphertext using your helper script
$ciphertext = python encrypt_seed.py

Write-Host "Generated ciphertext:" $ciphertext

# Step 2: Decrypt the seed
$decryptResponse = Invoke-RestMethod -Uri http://localhost:8000/decrypt-seed `
  -Method POST `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body (@{ciphertext=$ciphertext} | ConvertTo-Json)

Write-Host "Decrypted seed:" $decryptResponse.seed

# Step 3: Generate a 2FA code
$generateResponse = Invoke-RestMethod -Uri http://localhost:8000/generate-2fa -Method GET
Write-Host "Generated 2FA code:" $generateResponse.code

# Step 4: Verify the 2FA code
$verifyResponse = Invoke-RestMethod -Uri http://localhost:8000/verify-2fa `
  -Method POST `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body (@{code=$generateResponse.code} | ConvertTo-Json)

Write-Host "Verification result:" $verifyResponse.valid
