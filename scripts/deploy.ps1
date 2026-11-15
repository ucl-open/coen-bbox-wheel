param(
    # Root of the per-machine rig configuration directories. The rig workflow reads
    # <ConfigRoot>\<MACHINE-NAME>\rig.yml. In
    # Coen-Lab-Local with the lab's other local files (Pip, 29 Oct 2026); app-rig-setup
    # moved C:\RigConfigs there and left a link at the old place.
    [string]$ConfigRoot = "C:\Coen-Lab-Local\RigConfigs"
)

# A failed cmdlet or .NET call (rig.yml or the layout not written) stops the deploy with exit 1;
# without this it printed the error and went on to exit 0.
$ErrorActionPreference = 'Stop'

$scriptPath = $MyInvocation.MyCommand.Path
$scriptDirectory = Split-Path -Parent $scriptPath
Set-Location (Split-Path -Parent $scriptDirectory)

# A failing native command does not stop a PowerShell script, so each one is checked.
function Assert-Success([string]$Step) {
    if ($LASTEXITCODE -ne 0) { throw "$Step failed (exit code $LASTEXITCODE). The deploy is incomplete." }
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw "The 'uv' command was not found. See https://docs.astral.sh/uv/getting-started/installation/ for instructions."
}

Write-Output "Creating a Python environment..."
if (Test-Path -Path ./.venv) {
    Remove-Item ./.venv -Recurse -Force
}
&uv venv
Assert-Success "uv venv"
.\.venv\Scripts\Activate.ps1
Write-Output "Synchronizing environment..."
&uv sync --locked
Assert-Success "uv sync --locked"

if (-not (Get-Command dotnet -ErrorAction SilentlyContinue)) {
    throw "The 'dotnet' command was not found. Install the .NET SDK: https://dotnet.microsoft.com/download"
}

# Same name the rig workflow resolves at startup (Environment.MachineName).
$machineDirectory = Join-Path $ConfigRoot ([Environment]::MachineName)
Write-Output "Preparing the rig configuration directory $machineDirectory..."
New-Item -ItemType Directory -Path $machineDirectory -Force | Out-Null
$rigConfig = Join-Path $machineDirectory "rig.yml"
if (Test-Path -Path $rigConfig) {
    Write-Output "Keeping the existing $rigConfig"
} else {
    # The lab's one template (lib-open-rigs open_rigs\rigs\rig-template.yml, from the open-rigs this repo pins):
    # delete the devices a box lacks and fill in every CHANGE-ME.
    Copy-Item (Resolve-Path ".\.venv\Lib\site-packages\open_rigs\rigs\rig-template.yml").Path $rigConfig
    Write-Output "Created $rigConfig from the lab's rig template; keep the box's devices and fill in this rig's values there."
}

Write-Output "Creating a Bonsai environment and installing packages..."
# A missing script is a non-terminating error and leaves $LASTEXITCODE as it was, so check first.
# Setup.ps1 runs lib-open-rigs' setup-bonsai.ps1, which also puts config\main.layout (the camera
# preview and the camera's exposure and gain) in the editor's per-machine .bonsai\Settings\src\main.layout,
# keeping a different one beside it as main.saved.layout.
if (-not (Test-Path -Path .\.bonsai\Setup.ps1)) { throw ".bonsai\Setup.ps1 was not found. The deploy is incomplete." }
& .\.bonsai\Setup.ps1
Assert-Success "Installing Bonsai and its packages"

# The video is encoded by ffmpeg.exe, which LogVideoFfmpeg starts from PATH (or rig.yml's
# videoEncoder.ffmpegPath), with rig.yml's videoEncoder.codec (h264_qsv, Intel Quick Sync, on the
# boxes; libx264 when left out). Without ffmpeg.exe the workflow stops at Go.
$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
if (-not $ffmpeg) {
    Write-Warning "FFmpeg was not found on PATH. Install it with: winget install --id Gyan.FFmpeg -e, then open a new window."
} else {
    # Windows PowerShell turns a redirected native stderr line into an error, which 'Stop' would
    # make fatal: a machine without Quick Sync is only warned.
    $ErrorActionPreference = 'Continue'
    & $ffmpeg.Source -v error -f lavfi -i color=black:s=320x240 -frames:v 1 -c:v h264_qsv -f null - 2>$null
    $ErrorActionPreference = 'Stop'
    if ($LASTEXITCODE -eq 0) {
        Write-Output "FFmpeg found, Intel Quick Sync encoding works."
    } else {
        Write-Warning "FFmpeg is installed, but Intel Quick Sync (h264_qsv) does not work on this machine: with rig.yml's videoEncoder codec h264_qsv, the template's, the workflow stops when the first video opens, after Go. Set codec: libx264 in $rigConfig to encode in software."
    }
}
