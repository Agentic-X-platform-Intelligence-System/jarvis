# Run all Agile GitHub setup steps (repo-scoped + project if authorized)

param(
    [switch]$SkipProject,
    [int]$ProjectNumber = 0
)

$ErrorActionPreference = "Stop"
$ScriptDir = $PSScriptRoot

Write-Host "=== 1/4 Labels ==="
& "$ScriptDir\setup-labels.ps1"

Write-Host "`n=== 2/4 Milestones ==="
& "$ScriptDir\setup-milestones.ps1"

if (-not $SkipProject) {
    Write-Host "`n=== 3/4 GitHub Project ==="
    & "$ScriptDir\setup-github-project.ps1"
    $stateFile = Join-Path (Split-Path (Split-Path $ScriptDir -Parent) -Parent) ".github\project-state.json"
    if (Test-Path $stateFile) {
        $state = Get-Content $stateFile | ConvertFrom-Json
        if ($ProjectNumber -le 0) { $ProjectNumber = $state.projectNumber }
    }
} else {
    Write-Host "`n=== 3/4 GitHub Project (skipped) ==="
}

Write-Host "`n=== 4/4 Issues (epics + Sprint 1) ==="
& "$ScriptDir\setup-issues.ps1" -ProjectNumber $ProjectNumber

Write-Host "`nAll setup scripts finished. See docs/sprints/SPRINT0-CHECKLIST.md"
