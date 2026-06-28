# Create GitHub org project (requires: gh auth refresh -s read:project,project)

$ErrorActionPreference = "Stop"
$Org = "Agentic-X-platform-Intelligence-System"
$Repo = "$Org/jarvis"
$ProjectTitle = "AXIS/Jarvis Agile Board"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$StateFile = Join-Path $Root ".github\project-state.json"

Write-Host "Checking GitHub auth scopes..."
$auth = gh auth status 2>&1 | Out-String
if ($auth -notmatch "read:project|project") {
    Write-Warning @"
Missing project scopes. Run:
  gh auth refresh -s read:project,project
Then re-run this script.
"@
}

Write-Host "Listing existing projects..."
$existing = gh project list --owner $Org --format json 2>$null | ConvertFrom-Json
$project = $existing.projects | Where-Object { $_.title -eq $ProjectTitle } | Select-Object -First 1

if (-not $project) {
    Write-Host "Creating project: $ProjectTitle"
    $created = gh project create --owner $Org --title $ProjectTitle --format json | ConvertFrom-Json
    $projectNumber = $created.number
    $projectUrl = $created.url
} else {
    $projectNumber = $project.number
    $projectUrl = $project.url
    Write-Host "Project already exists: $projectUrl"
}

Write-Host "Linking repository $Repo..."
gh project link $projectNumber --owner $Org --repo $Repo 2>$null

$state = @{
    org = $Org
    repo = $Repo
    projectTitle = $ProjectTitle
    projectNumber = $projectNumber
    projectUrl = $projectUrl
    views = @("Backlog", "Sprint Board", "Roadmap", "Learning Tracker")
    configuredAt = (Get-Date -Format "yyyy-MM-dd")
    manualSteps = "See docs/GITHUB-PROJECTS.md for view and field configuration"
}
$state | ConvertTo-Json -Depth 4 | Set-Content $StateFile -Encoding UTF8

Write-Host @"

Project ready:
  Number: $projectNumber
  URL:    $projectUrl
  State:  $StateFile

Next steps (UI):
  1. Add custom fields: Status, Sprint, Story Points, Epic, Priority
  2. Create views per docs/GITHUB-PROJECTS.md
  3. Run setup-issues.ps1 with -ProjectNumber $projectNumber to link issues

"@
