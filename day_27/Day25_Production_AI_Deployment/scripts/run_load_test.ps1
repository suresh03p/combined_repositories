param([string]$BaseUrl = "http://localhost:8000", [int]$Count = 10)
$times = @()
for ($i = 0; $i -lt $Count; $i++) {
  $watch = [System.Diagnostics.Stopwatch]::StartNew()
  try { Invoke-RestMethod "$BaseUrl/health" | Out-Null; $ok = $true } catch { $ok = $false }
  $watch.Stop()
  $times += [pscustomobject]@{ Request = $i + 1; Milliseconds = $watch.ElapsedMilliseconds; Success = $ok }
}
$times | Format-Table
