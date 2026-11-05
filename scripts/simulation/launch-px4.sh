#!/usr/bin/env bash
# Run inside Ubuntu WSL. Python dependencies stay in the dedicated venv.
set -euo pipefail
root="${PX4_RESEARCH_ROOT:-$HOME/px4-research}"
model="${1:-x500}"
mode="${2:-gui}"
case "$model" in
  x500|rc_cessna|standard_vtol) ;;
  *) echo 'Model must be x500, rc_cessna or standard_vtol' >&2; exit 2 ;;
esac
case "$mode" in
  headless) export HEADLESS=1 ;;
  gui) unset HEADLESS; export QT_QPA_PLATFORM=xcb ;;
  *) echo 'Mode must be gui or headless' >&2; exit 2 ;;
esac
# Explicit D3D12 selection enables this host's Radeon 780M through WSLg.
# Override GALLIUM_DRIVER=llvmpipe for software rendering if necessary.
if [[ -e /dev/dxg ]]; then
  export GALLIUM_DRIVER="${GALLIUM_DRIVER:-d3d12}"
fi
export GZ_PARTITION="${GZ_PARTITION:-px4_research_${USER}}"
# shellcheck disable=SC1091
source "$root/.venv/bin/activate"
cd "$root/PX4-Autopilot"
# The explicit make variable also caps Ninja when launched without a terminal.
exec make -j4 j=4 px4_sitl "gz_${model}"
