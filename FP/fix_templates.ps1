$files = @(
    'x:\FP\garden\templates\garden\user_garden_final.html',
    'x:\FP\garden\templates\garden\user_garden_v3.html',
    'x:\FP\garden\templates\garden\user_garden.html',
    'x:\FP\garden\templates\garden\user_garden_fixed.html'
)

foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        $content = $content -replace 'status=="', 'status == "'
        Set-Content $file -Value $content -NoNewline
        Write-Host "Fixed: $file"
    }
}
