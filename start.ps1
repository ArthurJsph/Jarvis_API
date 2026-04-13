# Compatibility wrapper: delegates to scripts/start.ps1
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir/scripts/start.ps1" @args
