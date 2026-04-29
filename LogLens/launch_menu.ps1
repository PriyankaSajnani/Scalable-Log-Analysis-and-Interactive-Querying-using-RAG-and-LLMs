$ErrorActionPreference = "Stop"

# === Fix Path Resolution ===
$ScriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$logFile = "$ScriptDir\\loglens_run.log"
$venvPath = "$env:USERPROFILE\\LogLensEnv"
$reqFile = "$ScriptDir\\requirements.txt"

function Write-Log {
    param($message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $message" | Out-File -Append -FilePath $logFile
}

Write-Log "Script started."

function Confirm-Success {
    param($label)
    Write-Host "$label ✔" -ForegroundColor Green
    Write-Log "$label success."
}

# === 1. Check Python ===
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host Python_is_not_installed_Please_install_Python_first -ForegroundColor Red
    Write-Log "Python not found. Aborting."
    exit
}
Confirm-Success Python detected

# === 2. Check Ollama ===
$ollama = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollama) {
    Write-Host Ollama_is_not_installed_Please_install_Ollama_first -ForegroundColor Red
    Write-Log "Ollama not found. Aborting."
    exit
}
Confirm-Success Ollama detected

# === 3. Check LLaMA model ===
Write-Host "Checking for llama 3.2 model..." -ForegroundColor Yellow
$modelList = ollama ls 2>&1
if (-not ($modelList -like "*llama*3.2")) {
    Write-Host llama_3.2_model_not_found_Attempting_to_install -ForegroundColor Yellow
    Write-Log "llama 3.2 not found. Pulling..."
    $pullOutput = ollama pull llama:3.2 2>&1
    Write-Log "Pull output: $pullOutput"

    if ($LASTEXITCODE -ne 0) {
        Write-Host Failed_to_install_llama_3.2_model_automatically -ForegroundColor Red
        Write-Host Please_run_manually_ollama_pull_llama_3.2 -ForegroundColor Cyan
        Write-Log "llama:3.2 pull failed."
        Read-Host "Press Enter to continue..."
    } else {
        Confirm-Success llama 3.2 installed
    }
} else {
    Confirm-Success llama 3.2 already installed
}

# === 4. Create virtual environment ===
if (-not (Test-Path $venvPath\Scripts\Activate.ps1)) {
    Write-Host Creating_virtual_environment_at_$venvPath -ForegroundColor Yellow
    python -m venv $venvPath
    Confirm-Success Virtual environment created
} else {
    # Virtual environment already exists.
    Write-Host Virtual_environment_already_exists -ForegroundColor Cyan
}

# === 5. Activate and Install Requirements ===
Write-Host Installing_Python_libraries_from_requirements.txt -ForegroundColor Yellow

. $venvPath\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r $reqFile

Confirm-Success Libraries installed

# === 6. Final Welcome Message ===
Write-Host `n==========================================
Write-Host       Welcome to LogLens People!
Write-Host    Please refer to the README to get started.
Write-Host ==========================================

