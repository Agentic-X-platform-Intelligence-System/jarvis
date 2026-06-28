# Create epic and Sprint 1 story issues on GitHub

param(
    [int]$ProjectNumber = 0
)

$ErrorActionPreference = "Stop"
$Repo = "Agentic-X-platform-Intelligence-System/jarvis"
$Org = "Agentic-X-platform-Intelligence-System"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent

function Get-MilestoneNumber($title) {
    $milestones = gh api "repos/$Repo/milestones?state=open" --jq ".[] | select(.title==`"$title`") | .number" 2>$null
    return $milestones
}

function New-IssueIfMissing {
    param(
        [string]$Title,
        [string[]]$Labels,
        [string]$BodyFile,
        [string]$MilestoneTitle = ""
    )
    $existing = gh issue list --repo $Repo --search "in:title `"$Title`"" --json number,title --jq ".[] | select(.title==`"$Title`") | .number" 2>$null
    if ($existing) {
        Write-Host "Exists #$existing : $Title"
        return [int]$existing
    }
    $labelArg = ($Labels -join ",")
    $args = @(
        "issue", "create",
        "--repo", $Repo,
        "--title", $Title,
        "--label", $labelArg,
        "--body-file", $BodyFile
    )
    if ($MilestoneTitle) {
        $mn = Get-MilestoneNumber $MilestoneTitle
        if ($mn) { $args += @("--milestone", $MilestoneTitle) }
    }
    $url = & gh @args
    $num = ($url -replace ".*issues/", "").Trim()
    Write-Host "Created #$num : $Title"
    return [int]$num
}

function Add-ToProject {
    param([int]$IssueNumber)
    if ($ProjectNumber -le 0) { return }
    gh project item-add $ProjectNumber --owner $Org --url "https://github.com/$Repo/issues/$IssueNumber" 2>$null
}

Write-Host "Creating epics..."
$epics = @(
    @{ Title = "Epic 1: P1 - stem Kernel & Jarvis CLI"; File = "E1-stem-cli.md"; Labels = @("epic","p1-high","stem","jarvis"); Milestone = "M1 — stem + CLI" },
    @{ Title = "Epic 2: P1 - Aura Voice Migration"; File = "E2-aura-voice.md"; Labels = @("epic","p1-high","aura","stem"); Milestone = "M2 — Aura voice" },
    @{ Title = "Epic 3: P2 - Edith RAG Knowledge Base"; File = "E3-edith-rag.md"; Labels = @("epic","p2-medium","edith"); Milestone = "M3 — Edith RAG" },
    @{ Title = "Epic 4: P3 - Karen Code Review Bot"; File = "E4-karen-review.md"; Labels = @("epic","p2-medium","karen"); Milestone = "M4 — Karen review" },
    @{ Title = "Epic 5: P4 - Friday Research Agent"; File = "E5-friday-research.md"; Labels = @("epic","p2-medium","friday"); Milestone = "M5 — Friday research" },
    @{ Title = "Epic 6: P5 - Cognis Java Migrator"; File = "E6-cognis-migrator.md"; Labels = @("epic","p2-medium","cognis"); Milestone = "M6 — Cognis migrator" },
    @{ Title = "Epic 7: P6 - Kinetix Dev Crew"; File = "E7-kinetix-crew.md"; Labels = @("epic","p2-medium","kinetix"); Milestone = "M7 — Kinetix crew" },
    @{ Title = "Epic 8: P7 - Aero Production API"; File = "E8-aero-api.md"; Labels = @("epic","p2-medium","aero"); Milestone = "M8 — Aero API" },
    @{ Title = "Epic 9: P8 - Full-Stack AI SaaS"; File = "E9-saas-capstone.md"; Labels = @("epic","p2-medium","aero","jarvis","aura"); Milestone = "M9 — P8 SaaS" }
)

$epicNumbers = @{}
foreach ($e in $epics) {
    $body = Join-Path $Root ".github\epics\$($e.File)"
    $num = New-IssueIfMissing -Title $e.Title -Labels $e.Labels -BodyFile $body -MilestoneTitle $e.Milestone
    $epicNumbers[$e.Title] = $num
    Add-ToProject -IssueNumber $num
}

$e1 = $epicNumbers["Epic 1: P1 - stem Kernel & Jarvis CLI"]

Write-Host "Creating Sprint 1 stories..."
$stories = @(
    @{ Title = "[Story] Multi-provider LLM interface"; File = "S1.1-llm-providers.md"; Labels = @("story","p1-high","stem","sprint-1") },
    @{ Title = "[Story] Hybrid LLM router"; File = "S1.2-hybrid-router.md"; Labels = @("story","p1-high","stem","sprint-1") },
    @{ Title = "[Story] Pydantic tool framework"; File = "S1.3-tool-framework.md"; Labels = @("story","p1-high","stem","sprint-1") },
    @{ Title = "[Story] P1 tools — filesystem"; File = "S1.4-filesystem-tools.md"; Labels = @("story","p1-high","stem","sprint-1") },
    @{ Title = "[Story] P1 tools — shell and web"; File = "S1.5-shell-web-tools.md"; Labels = @("story","p1-high","stem","sprint-1") }
)

foreach ($s in $stories) {
    $bodyPath = Join-Path $Root ".github\stories\$($s.File)"
    $body = Get-Content $bodyPath -Raw
    $body += "`n`n**Parent Epic:** #$e1`n"
    $tmp = Join-Path $env:TEMP "axis-story-$($s.File)"
    Set-Content $tmp $body -Encoding UTF8
    $num = New-IssueIfMissing -Title $s.Title -Labels $s.Labels -BodyFile $tmp -MilestoneTitle "M1 — stem + CLI"
    Add-ToProject -IssueNumber $num
}

# Save issue map for reference
$mapFile = Join-Path $Root ".github\issue-map.json"
@{
    epics = $epicNumbers
    sprint1Epic = $e1
    createdAt = (Get-Date -Format "yyyy-MM-dd")
} | ConvertTo-Json -Depth 4 | Set-Content $mapFile -Encoding UTF8

Write-Host "Done. Issue map: $mapFile"
if ($ProjectNumber -le 0) {
    Write-Host "Tip: re-run with -ProjectNumber <N> after setup-github-project.ps1"
}
