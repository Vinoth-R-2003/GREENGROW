$file = 'x:\FP\garden\templates\garden\journal_list.html'

if (Test-Path $file) {
    $content = Get-Content $file -Raw
    # Fix the multi-line template tag
    $content = $content -replace '\{\{\s*\r?\n\s*entry\.entry_date\|date:"M d, Y"\s*\}\}', '{{ entry.entry_date|date:"M d, Y" }}'
    Set-Content $file -Value $content -NoNewline
    Write-Host "Fixed: $file"
}
