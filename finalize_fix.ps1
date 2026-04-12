# Finalize AI Bug Fix - Test, Commit, and Push Script
# This script assumes AI fixes have been applied to a local repository
# It runs tests, commits changes if tests pass, and pushes the branch to origin

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoPath,

    [Parameter(Mandatory=$true)]
    [string]$BranchName,

    [Parameter(Mandatory=$true)]
    [string]$BugDescription
)

# Change to repo directory
Set-Location $RepoPath

# Check if we're on the correct branch
$currentBranch = git branch --show-current
if ($currentBranch -ne $BranchName) {
    Write-Host "Warning: Currently on branch '$currentBranch', expected '$BranchName'"
    # Switch to the branch
    git checkout $BranchName
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to checkout branch '$BranchName'"
        exit 1
    }
}

# Run tests
Write-Host "Running tests..."
$testResult = & python -m pytest -q 2>&1
$testExitCode = $LASTEXITCODE

if ($testExitCode -eq 0) {
    $testStatus = "passed"
} elseif ($testExitCode -eq 5) {
    $testStatus = "skipped"  # No tests found
} else {
    $testStatus = "failed"
}

Write-Host "Test status: $testStatus"

if ($testStatus -notin @("passed", "skipped")) {
    Write-Host "Tests failed. Not committing or pushing changes."
    exit 1
}

# Get changed files
$changedFiles = git diff --name-only HEAD
if ($changedFiles) {
    # Create summary file
    $summaryFileName = "AI_FIX_SUMMARY_$($BranchName -replace '[^A-Za-z0-9_.-]', '-')_$(Get-Date -Format 'yyyyMMdd_HHmmss').md"
    $summaryContent = @"
# AI Fix Summary for branch `$BranchName`

**Bug description:** $BugDescription

## Changed files
$($changedFiles | ForEach-Object { "- `$_`n" })

## Notes
This branch was created by the AI Autonomous Bug Fixing System.
Review the generated patch/diff and push this branch when ready.
"@

    $summaryContent | Out-File -FilePath $summaryFileName -Encoding UTF8
    Write-Host "Created summary file: $summaryFileName"
}

# Add all changes
git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to add files"
    exit 1
}

# Check status
Write-Host "Git status:"
git status --short

# Check if there are changes to commit
$statusOutput = git status --porcelain
if (-not $statusOutput) {
    Write-Host "No changes to commit."
    exit 0
}

# Commit changes
$commitMessage = "AI fix branch $BranchName`: $BugDescription"
Write-Host "Committing changes with message: $commitMessage"
git commit -m $commitMessage
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to commit changes"
    exit 1
}

# Push branch
Write-Host "Pushing branch $BranchName to origin..."
git push --set-upstream origin $BranchName
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to push branch '$BranchName'"
    exit 1
}

Write-Host "Fix finalization complete!"