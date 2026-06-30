#!/usr/bin/env bash
set -euo pipefail

# Session-local cache/temp redirection for the shared server account.
# Use with:
#   source /mnt/mewdata/hcx/BCBT/tools/setup_codamosa_env.sh

ROOT="/mnt/mewdata/hcx/card_cache"

mkdir -p "$ROOT/.cache/pip"
mkdir -p "$ROOT/.conda/pkgs"
mkdir -p "$ROOT/.conda/envs"
mkdir -p "$ROOT/tmp"

export PIP_CACHE_DIR="$ROOT/.cache/pip"
export CONDA_PKGS_DIRS="$ROOT/.conda/pkgs"
export CONDA_ENVS_DIRS="$ROOT/.conda/envs"
export TMPDIR="$ROOT/tmp"
export TEMP="$ROOT/tmp"
export TMP="$ROOT/tmp"

echo "[setup_codamosa_env] PIP_CACHE_DIR=$PIP_CACHE_DIR"
echo "[setup_codamosa_env] CONDA_PKGS_DIRS=$CONDA_PKGS_DIRS"
echo "[setup_codamosa_env] CONDA_ENVS_DIRS=$CONDA_ENVS_DIRS"
echo "[setup_codamosa_env] TMPDIR=$TMPDIR"
