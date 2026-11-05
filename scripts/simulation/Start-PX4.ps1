param(
    [ValidateSet('x500', 'rc_cessna', 'standard_vtol')]
    [string]$Model = 'x500',
    [switch]$Headless
)
$mode = if ($Headless) { 'headless' } else { 'gui' }
wsl.exe -d Ubuntu -- bash /home/alfred/px4-research/bin/launch-px4.sh $Model $mode
exit $LASTEXITCODE
