#!/usr/bin/env bash
# Setup a Python 3.14 virtualenv that loads ROOT on activation.
#
# Behavior:
#  - Prefer an existing `python3.14` on PATH.
#  - Fall back to Homebrew python@3.14 path.
#  - Create venv at `.venv_py314` (ask before overwriting).
#  - Append `thisroot.sh` sourcing to the venv `activate` script so ROOT is available.

set -euo pipefail

VENV_DIR=".venv_py314"

echo "==> Locating a Python 3.14 executable..."
PYTHON_EXE=""
if command -v python3.14 >/dev/null 2>&1; then
    PYTHON_EXE="$(command -v python3.14)"
elif [ -x "/opt/homebrew/opt/python@3.14/bin/python3.14" ]; then
    PYTHON_EXE="/opt/homebrew/opt/python@3.14/bin/python3.14"
elif command -v python >/dev/null 2>&1 && python --version 2>&1 | grep -q "Python 3.14"; then
    PYTHON_EXE="$(command -v python)"
else
    echo "No python3.14 found on PATH. Install it with Homebrew: 'brew install python@3.14' or use pyenv to install a 3.14.x release." >&2
    exit 1
fi

echo "Using Python: ${PYTHON_EXE} ($(${PYTHON_EXE} --version 2>&1))"

if [ -d "${VENV_DIR}" ]; then
    read -r -p "Virtualenv ${VENV_DIR} already exists. Remove and recreate? [y/N] " yn
    case "$yn" in
        [Yy]*) rm -rf "${VENV_DIR}" ;;
        *) echo "Aborting."; exit 0 ;;
    esac
fi

echo "Creating virtualenv at ${VENV_DIR}..."
"${PYTHON_EXE}" -m venv "${VENV_DIR}"

echo "Upgrading pip in venv..."
"${VENV_DIR}/bin/python" -m pip install --upgrade pip >/dev/null

# Find ROOT prefix via root-config (if available)
if command -v root-config >/dev/null 2>&1; then
    ROOT_PREFIX="$(root-config --prefix)"
    THISROOT="${ROOT_PREFIX}/bin/thisroot.sh"
    if [ -f "${THISROOT}" ]; then
        echo "Configuring venv to source ROOT's thisroot.sh on activation..."
        printf '\n# Automatically enable ROOT environment\nif [ -f "%s" ]; then\n  source "%s"\nfi\n' "${THISROOT}" "${THISROOT}" >> "${VENV_DIR}/bin/activate"
        echo "Appended sourcing of ${THISROOT} to ${VENV_DIR}/bin/activate"
    else
        echo "root-config found but thisroot.sh not at ${THISROOT}; please verify your ROOT installation." >&2
    fi
else
    echo "root-config not found. Ensure ROOT is installed and root-config is on PATH." >&2
fi

cat <<'EOF'
Done.

How to use:
  source .venv_py314/bin/activate
  # the venv activation will also source ROOT if available
  python -c "import sys; print(sys.executable); import ROOT; print(ROOT.gROOT.GetVersion())"

If you still see segfaults or version mismatch errors, ensure the Python interpreter in the venv is a standard (GIL-enabled) CPython 3.14 release (not a GIL-free/dev build like 3.14t-dev).
EOF

exit 0
