#Requires -Version 5.1

param(
    [Parameter(Mandatory = $true)]
    [int]$TargetPid,

    [int]$DurationSeconds = 300,
    [int]$SampleMs = 200,
    [int]$CpuThresholdPercent = 5,
    [int]$DumpCount = 10,
    [string]$ProcDumpPath = 'C:\bin\sysin\procdump64.exe',
    [string]$OutputRoot = ''
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $ProcDumpPath)) {
    throw "ProcDump not found: $ProcDumpPath"
}

$scriptRoot = Split-Path -Parent $PSCommandPath
$workspaceRoot = Resolve-Path -LiteralPath (Join-Path $scriptRoot '..\..\..')
if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path $workspaceRoot 'workspaces\workspace\state\diagnostics'
}

$process = Get-Process -Id $TargetPid -ErrorAction Stop
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$outDir = Join-Path $OutputRoot "pid-$TargetPid-cpu-spikes-$stamp"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$samplePath = Join-Path $outDir 'thread-cpu-samples.csv'
$summaryPath = Join-Path $outDir 'thread-cpu-summary.txt'
$procDumpLog = Join-Path $outDir 'procdump.log'
$procDumpErr = Join-Path $outDir 'procdump.err.log'
$dumpBase = Join-Path $outDir 'emule_cpu.dmp'

$logical = (Get-CimInstance Win32_ComputerSystem).NumberOfLogicalProcessors
'UtcTime,ElapsedMs,ProcessPctOneCore,ProcessPctAllCores,TidDec,TidHex,DeltaMs,ThreadPctOneCore,State,WaitReason' |
    Set-Content -Encoding UTF8 -LiteralPath $samplePath

$procDumpArgs = @(
    '-accepteula',
    '-ma',
    '-n', [string]$DumpCount,
    '-s', '1',
    '-c', [string]$CpuThresholdPercent,
    [string]$TargetPid,
    $dumpBase
)

$procDump = Start-Process -FilePath $ProcDumpPath -ArgumentList $procDumpArgs -RedirectStandardOutput $procDumpLog -RedirectStandardError $procDumpErr -WindowStyle Hidden -PassThru

Write-Host "PID=$TargetPid"
Write-Host "Process=$($process.Path)"
Write-Host "Output=$outDir"
Write-Host "ProcDumpPid=$($procDump.Id)"
Write-Host "Sampling ${DurationSeconds}s at ${SampleMs}ms; ProcDump threshold=${CpuThresholdPercent}% system, dumps=$DumpCount"

$prevProc = Get-Process -Id $TargetPid -ErrorAction Stop
$prevProcCpu = $prevProc.TotalProcessorTime.TotalMilliseconds
$prev = @{}
foreach ($thread in $prevProc.Threads) {
    $prev[[int]$thread.Id] = [double]$thread.TotalProcessorTime.TotalMilliseconds
}

$end = (Get-Date).AddSeconds($DurationSeconds)
while ((Get-Date) -lt $end) {
    $before = Get-Date
    Start-Sleep -Milliseconds $SampleMs
    $after = Get-Date
    $elapsedMs = ($after - $before).TotalMilliseconds

    $current = Get-Process -Id $TargetPid -ErrorAction Stop
    $procCpu = $current.TotalProcessorTime.TotalMilliseconds
    $procPctOneCore = (($procCpu - $prevProcCpu) / $elapsedMs) * 100.0

    foreach ($thread in $current.Threads) {
        $tid = [int]$thread.Id
        $now = [double]$thread.TotalProcessorTime.TotalMilliseconds
        $old = if ($prev.ContainsKey($tid)) { $prev[$tid] } else { $now }
        $delta = $now - $old
        if ($delta -le 0) {
            continue
        }

        $waitReason = ''
        if ($thread.ThreadState -eq 'Wait') {
            $waitReason = [string]$thread.WaitReason
        }

        $line = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}' -f `
            (Get-Date).ToUniversalTime().ToString('o'),
            [math]::Round($elapsedMs, 1),
            [math]::Round($procPctOneCore, 1),
            [math]::Round($procPctOneCore / [double]$logical, 1),
            $tid,
            ('0x{0:x}' -f $tid),
            [math]::Round($delta, 1),
            [math]::Round(($delta / $elapsedMs) * 100.0, 1),
            [string]$thread.ThreadState,
            $waitReason
        Add-Content -Encoding UTF8 -LiteralPath $samplePath -Value $line
    }

    $prev = @{}
    foreach ($thread in $current.Threads) {
        $prev[[int]$thread.Id] = [double]$thread.TotalProcessorTime.TotalMilliseconds
    }
    $prevProcCpu = $procCpu
}

$csv = Import-Csv -LiteralPath $samplePath
"LogicalProcessors=$logical" | Set-Content -Encoding UTF8 -LiteralPath $summaryPath
"SampleRows=$($csv.Count)" | Add-Content -Encoding UTF8 -LiteralPath $summaryPath
"ProcessStillRunning=$([bool](Get-Process -Id $TargetPid -ErrorAction SilentlyContinue))" | Add-Content -Encoding UTF8 -LiteralPath $summaryPath
"ProcDumpStillRunning=$(-not $procDump.HasExited)" | Add-Content -Encoding UTF8 -LiteralPath $summaryPath
'' | Add-Content -Encoding UTF8 -LiteralPath $summaryPath
'Top individual sample windows:' | Add-Content -Encoding UTF8 -LiteralPath $summaryPath
$csv |
    Sort-Object { [double]$_.DeltaMs } -Descending |
    Select-Object -First 40 |
    Format-Table -AutoSize |
    Out-String |
    Add-Content -Encoding UTF8 -LiteralPath $summaryPath

'' | Add-Content -Encoding UTF8 -LiteralPath $summaryPath
'Aggregate by thread:' | Add-Content -Encoding UTF8 -LiteralPath $summaryPath
$csv |
    Group-Object TidDec,TidHex |
    ForEach-Object {
        $parts = $_.Name -split ', '
        [pscustomobject]@{
            TidDec = $parts[0]
            TidHex = $parts[1]
            Samples = $_.Count
            TotalDeltaMs = [math]::Round(($_.Group | Measure-Object -Property DeltaMs -Sum).Sum, 1)
            MaxDeltaMs = [math]::Round(($_.Group | Measure-Object -Property DeltaMs -Maximum).Maximum, 1)
            MaxProcPctOneCore = [math]::Round(($_.Group | Measure-Object -Property ProcessPctOneCore -Maximum).Maximum, 1)
        }
    } |
    Sort-Object TotalDeltaMs -Descending |
    Select-Object -First 30 |
    Format-Table -AutoSize |
    Out-String |
    Add-Content -Encoding UTF8 -LiteralPath $summaryPath

Get-ChildItem -LiteralPath $outDir -Filter '*.dmp' |
    Select-Object Name,Length,LastWriteTime |
    Format-Table -AutoSize |
    Out-String |
    Add-Content -Encoding UTF8 -LiteralPath $summaryPath

Get-Content -LiteralPath $summaryPath
Write-Host "SAMPLE_LOG=$samplePath"
Write-Host "PROCDUMP_LOG=$procDumpLog"
Write-Host "PROCDUMP_ERR_LOG=$procDumpErr"
