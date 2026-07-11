# Create GitHub milestones M1-M9

$ErrorActionPreference = "Continue"
$Repo = "Agentic-X-platform-Intelligence-System/jarvis"

$milestones = @(
    @{ Title = "M1 - stem + CLI"; Due = "2026-07-17"; Desc = "Epic E1: stem kernel and Jarvis CLI" },
    @{ Title = "M2 - Aura voice"; Due = "2026-07-24"; Desc = "Epic E2: Aura voice on shared stem" },
    @{ Title = "M3 - Edith RAG"; Due = "2026-08-07"; Desc = "Epic E3: RAG knowledge base" },
    @{ Title = "M4 - Karen review"; Due = "2026-08-21"; Desc = "Epic E4: Code review bot" },
    @{ Title = "M5 - Friday research"; Due = "2026-09-04"; Desc = "Epic E5: Research agent" },
    @{ Title = "M6 - Cognis migrator"; Due = "2026-09-18"; Desc = "Epic E6: Java migrator" },
    @{ Title = "M7 - Kinetix crew"; Due = "2026-09-25"; Desc = "Epic E7: Dev crew" },
    @{ Title = "M8 - Aero API"; Due = "2026-10-02"; Desc = "Epic E8: Production API" },
    @{ Title = "M9 - P8 SaaS"; Due = "2026-10-09"; Desc = "Epic E9: SaaS capstone" }
)

foreach ($m in $milestones) {
    Write-Host "Creating milestone: $($m.Title)"
    gh api repos/$Repo/milestones -f title="$($m.Title)" -f due_on="$($m.Due)T23:59:59Z" -f description="$($m.Desc)" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  (may already exist)"
    }
}

Write-Host "Milestones configured."
