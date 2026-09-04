$ErrorActionPreference = "Stop"

Import-Module Microsoft.PowerShell.Management -ErrorAction SilentlyContinue
Import-Module Microsoft.PowerShell.Utility -ErrorAction SilentlyContinue

$AppName = "AI Resume Analyser"
$ScriptPath = if ($PSCommandPath) { $PSCommandPath } else { $MyInvocation.MyCommand.Path }
$ToolsDir = [System.IO.Path]::GetDirectoryName($ScriptPath)
$Root = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine($ToolsDir, ".."))
$PortableDir = Join-Path $Root ".portable"
$CacheDir = Join-Path $PortableDir "cache"
$NodeVersion = "22.11.0"
$MachineArch = if ($env:PROCESSOR_ARCHITEW6432) { $env:PROCESSOR_ARCHITEW6432 } else { $env:PROCESSOR_ARCHITECTURE }
$NodeArch = if ($MachineArch -eq "ARM64") { "arm64" } else { "x64" }
$NodeArchive = "node-v$NodeVersion-win-$NodeArch.zip"
$NodeUrl = "https://nodejs.org/dist/v$NodeVersion/$NodeArchive"
$NodeHome = Join-Path $PortableDir "node-v$NodeVersion-win-$NodeArch"
$NodeExe = Join-Path $NodeHome "node.exe"
$NpmCmd = Join-Path $NodeHome "npm.cmd"
$StampFile = Join-Path $Root "node_modules\.portable-install-stamp"
$DefaultPort = 5173

function Write-Step($Message) {
  Write-Host ""
  Write-Host "==> $Message"
}

function Require-File($Path, $Message) {
  if (-not (Test-Path $Path)) {
    throw $Message
  }
}

function Ensure-Tls12 {
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
}

function Invoke-Checked($File, [string[]]$ArgsList) {
  & $File @ArgsList
  if ($LASTEXITCODE -ne 0) {
    throw "Command failed: $File $($ArgsList -join ' ')"
  }
}

function Get-FileHashText($Path) {
  return (Get-FileHash -Algorithm SHA256 $Path).Hash.ToLowerInvariant()
}

function Expand-ZipArchive($ArchivePath, $DestinationPath) {
  Add-Type -AssemblyName System.IO.Compression.FileSystem
  New-Item -ItemType Directory -Force -Path $DestinationPath | Out-Null
  [System.IO.Compression.ZipFile]::ExtractToDirectory($ArchivePath, $DestinationPath)
}

function Ensure-Node {
  New-Item -ItemType Directory -Force -Path $PortableDir, $CacheDir | Out-Null

  if (Test-Path $NodeExe) {
    Write-Host "Portable Node ready: $NodeExe"
    return
  }

  Write-Step "Downloading portable Node.js $NodeVersion"
  Ensure-Tls12
  $ArchivePath = Join-Path $CacheDir $NodeArchive
  if (-not (Test-Path $ArchivePath)) {
    $PartialArchivePath = "$ArchivePath.part"
    if (Test-Path $PartialArchivePath) {
      Remove-Item -Force $PartialArchivePath
    }
    Invoke-WebRequest -Uri $NodeUrl -OutFile $PartialArchivePath -UseBasicParsing
    Move-Item -Force $PartialArchivePath $ArchivePath
  }

  $ExtractTmp = Join-Path $CacheDir "node-extract"
  if (Test-Path $ExtractTmp) {
    Remove-Item -Recurse -Force $ExtractTmp
  }

  Expand-ZipArchive -ArchivePath $ArchivePath -DestinationPath $ExtractTmp
  $ExtractedNode = Join-Path $ExtractTmp "node-v$NodeVersion-win-$NodeArch"
  Require-File $ExtractedNode "Downloaded Node archive did not contain expected folder."

  if (Test-Path $NodeHome) {
    Remove-Item -Recurse -Force $NodeHome
  }
  Move-Item $ExtractedNode $NodeHome
  Remove-Item -Recurse -Force $ExtractTmp
  Require-File $NodeExe "Portable Node install failed."
}

function Get-FreePort([int]$StartPort) {
  for ($Port = $StartPort; $Port -le 8999; $Port++) {
    $Listener = $null
    try {
      $Listener = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Parse("127.0.0.1"), $Port)
      $Listener.Start()
      return $Port
    }
    catch {
    }
    finally {
      if ($null -ne $Listener) {
        $Listener.Stop()
      }
    }
  }
  throw "No free local port found from $StartPort to 8999."
}

function Ensure-Dependencies {
  Require-File (Join-Path $Root "package.json") "Missing package.json. Run START.bat from the project root."

  $PackageHash = Get-FileHashText (Join-Path $Root "package.json")
  $LockPath = Join-Path $Root "package-lock.json"
  if (Test-Path $LockPath) {
    $PackageHash = "$PackageHash-$((Get-FileHashText $LockPath))"
  }

  $OldHash = ""
  if (Test-Path $StampFile) {
    $OldHash = (Get-Content $StampFile -Raw).Trim()
  }

  $ViteCmd = Join-Path $Root "node_modules\.bin\vite.cmd"
  if ((Test-Path $ViteCmd) -and ($OldHash -eq $PackageHash)) {
    Write-Host "Dependencies already ready."
    return
  }

  Write-Step "Installing project dependencies"
  Push-Location $Root
  try {
    if (Test-Path $LockPath) {
      & $NpmCmd ci --no-audit --fund=false
      if ($LASTEXITCODE -ne 0) {
        Write-Host "npm ci failed. Rebuilding node_modules with npm install..."
        if (Test-Path (Join-Path $Root "node_modules")) {
          Remove-Item -Recurse -Force (Join-Path $Root "node_modules")
        }
        Invoke-Checked -File $NpmCmd -ArgsList @("install", "--no-audit", "--fund=false")
      }
    }
    else {
      Invoke-Checked -File $NpmCmd -ArgsList @("install", "--no-audit", "--fund=false")
    }
    New-Item -ItemType Directory -Force -Path ([System.IO.Path]::GetDirectoryName($StampFile)) | Out-Null
    Set-Content -Path $StampFile -Value $PackageHash -Encoding ASCII
  }
  finally {
    Pop-Location
  }
}

try {
  Set-Location $Root
  Write-Host ""
  Write-Host $AppName
  Write-Host "=========================="
  Write-Host "Project: $Root"

  Ensure-Node
  $env:PATH = "$NodeHome;$env:PATH"
  Write-Host "Node: $(& $NodeExe --version)"
  Write-Host "npm:  $(& $NpmCmd --version)"

  Ensure-Dependencies

  $Port = Get-FreePort $DefaultPort
  $Url = "http://127.0.0.1:$Port"
  Write-Step "Starting app"
  Write-Host "App: $Url"
  Write-Host "Local analysis mode. No API key needed."
  Start-Process $Url

  Push-Location $Root
  try {
    Invoke-Checked -File $NpmCmd -ArgsList @("run", "client", "--", "--host", "127.0.0.1", "--port", "$Port")
  }
  finally {
    Pop-Location
  }
}
catch {
  Write-Host ""
  Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
  exit 1
}
