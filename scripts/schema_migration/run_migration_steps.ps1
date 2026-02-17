<#
Simple PowerShell helper to run schema migration steps in order.
Edit the $dbUser and $dbName variables or pass credentials as needed.
#>
param(
  [string]$dbUser = "root",
  [string]$dbName = "venora_db",
  [string]$password = "",
  [switch]$WhatIfRun
)

function RunSqlFile($file) {
  Write-Host "=== Running $file ==="
  $cmd = "mysql -u $dbUser -p$($password) $dbName < `"$file`""
  if ($WhatIfRun) { Write-Host "WhatIf: $cmd"; return }
  Write-Host "Executing..."
  iex $cmd
}

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
RunSqlFile (Join-Path $root "00_checks.sql")
Write-Host "Review the output. Fix duplicates/orphans before proceeding."
if (-not $WhatIfRun) {
  RunSqlFile (Join-Path $root "06_convert_to_innodb.sql")
  RunSqlFile (Join-Path $root "05_archive_orphans.sql")
  RunSqlFile (Join-Path $root "04_dedupe_and_replace.sql")
  RunSqlFile (Join-Path $root "01_add_uniques.sql")
  RunSqlFile (Join-Path $root "02_add_foreign_keys.sql")
}
Write-Host "Done. Verify results and optionally run 03_convert_enums.sql manually after review."
