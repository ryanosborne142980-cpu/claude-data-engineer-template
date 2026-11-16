<#
.SYNOPSIS
    Copies the data-engineering agent template into a repo.

.DESCRIPTION
    Copies template/ into -Target, including only the .claude/rules/<stack>.md
    files you select. It never overwrites existing files: they are skipped, or with -Force
    written next to the original as <name>.template-new so you can merge by hand.
    .gitignore.de is merged into the target's .gitignore (new lines only).

.EXAMPLE
    .\new-de-repo.ps1 -Target C:\dev\my-repo -Stack sqlserver,python

.EXAMPLE
    .\new-de-repo.ps1 -Target C:\dev\my-repo -Stack all -Force
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$Target,

    [ValidateSet('sqlserver', 'databricks', 'azure', 'python', 'all', 'none')]
    [string[]]$Stack = @('python'),

    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$allStacks = @('sqlserver', 'databricks', 'azure', 'python')
if ($Stack -contains 'all') { $Stack = $allStacks }
if ($Stack -contains 'none') { $Stack = @() }

$templateRoot = Join-Path $PSScriptRoot 'template'
if (-not (Test-Path $templateRoot)) { throw "Template folder not found: $templateRoot" }
if (-not (Test-Path $Target)) { New-Item -ItemType Directory -Path $Target | Out-Null }
$Target = (Resolve-Path $Target).Path
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$written = @()
$skipped = @()
$sideFiles = @()

# Stack rules live in .claude/rules/<stack>.md; copy only the selected ones.
$rulesDir = Join-Path $templateRoot '.claude\rules'
$files = Get-ChildItem -Path $templateRoot -Recurse -File -Force | Where-Object {
    $_.Name -ne '.gitignore.de' -and $_.Directory.Name -ne '__pycache__' -and
    -not ($_.DirectoryName -eq $rulesDir -and $Stack -notcontains $_.BaseName)
}

foreach ($file in $files) {
    $rel = $file.FullName.Substring($templateRoot.Length).TrimStart('\', '/')
    $dest = Join-Path $Target $rel
    $content = [IO.File]::ReadAllText($file.FullName)

    if (Test-Path $dest) {
        if (-not $Force) { $skipped += $rel; continue }
        $dest = "$dest.template-new"
        $sideFiles += "$rel.template-new"
    }
    $dir = Split-Path $dest -Parent
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
    [IO.File]::WriteAllText($dest, $content, $utf8NoBom)
    $written += $dest
}

# Merge .gitignore: append only entries that are not already present.
$gitignore = Join-Path $Target '.gitignore'
$snippet = Get-Content (Join-Path $templateRoot '.gitignore.de')
$existing = @()
if (Test-Path $gitignore) { $existing = Get-Content $gitignore | ForEach-Object { $_.Trim() } }
$newEntries = $snippet | Where-Object { $_.Trim() -and -not $_.Trim().StartsWith('#') -and ($existing -notcontains $_.Trim()) }
if ($newEntries) {
    $toAppend = $snippet | Where-Object { -not $_.Trim() -or $_.Trim().StartsWith('#') -or ($existing -notcontains $_.Trim()) }
    $prefix = ''
    if ((Test-Path $gitignore) -and (Get-Item $gitignore).Length -gt 0) { $prefix = "`n" }
    [IO.File]::AppendAllText($gitignore, $prefix + (($toAppend -join "`n").TrimEnd()) + "`n", $utf8NoBom)
    Write-Host ".gitignore: added $(@($newEntries).Count) entries"
} else {
    Write-Host '.gitignore: already up to date'
}

$stackLabel = if ($Stack.Count) { $Stack -join ', ' } else { 'none' }
Write-Host "Stacks: $stackLabel"
Write-Host "Written: $($written.Count) file(s)"
if ($skipped) {
    Write-Host "Skipped (already exist; rerun with -Force to get .template-new copies):" -ForegroundColor Yellow
    $skipped | ForEach-Object { Write-Host "  $_" }
}
if ($sideFiles) {
    Write-Host 'Merge these by hand, then delete them:' -ForegroundColor Yellow
    $sideFiles | ForEach-Object { Write-Host "  $_" }
}

# docs/ stubs contain intentional entry templates, so only report the instruction files.
$todo = $written | Where-Object { $_ -match '\.md(\.template-new)?$' -and $_ -notmatch '[\\/]docs[\\/]' } |
    ForEach-Object { Select-String -Path $_ -Pattern '\{\{' }
if ($todo) {
    Write-Host "`nFill in these placeholders:" -ForegroundColor Cyan
    $todo | ForEach-Object {
        $relPath = $_.Path.Substring($Target.Length).TrimStart('\', '/')
        Write-Host ("  {0}:{1}  {2}" -f $relPath, $_.LineNumber, $_.Line.Trim())
    }
}
