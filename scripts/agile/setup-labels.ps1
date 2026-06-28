# Setup GitHub labels from .github/labels.json

$ErrorActionPreference = "Stop"
$Repo = "Agentic-X-platform-Intelligence-System/jarvis"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$LabelsFile = Join-Path $Root ".github\labels.json"

$labels = Get-Content $LabelsFile -Raw | ConvertFrom-Json

foreach ($label in $labels) {
    Write-Host "Ensure label: $($label.name)"
    gh label create $label.name --repo $Repo --color $label.color --description $label.description --force
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create label: $($label.name)"
    }
}

Write-Host "Done. $(($labels | Measure-Object).Count) labels configured."
