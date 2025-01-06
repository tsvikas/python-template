#!/usr/bin/env bash
set -e

# git init & initial commit
git init -q
git add --all
git reset init.sh
git commit -m "initial commit" -q

# install venv
uv python pin python3.{{python_minor}}
uv sync
git add uv.lock .python-version
git commit -m "chore: uv sync" -q

# pre-commit update
uv run pre-commit autoupdate -j "$(nproc)"
git add .pre-commit-config.yaml
git commit -m "chore: pre-commit update" -q

# pre-commit install
uv run pre-commit install > /dev/null
uv run pre-commit run --all-files

echo "use 'gh repo create' to set this repo on GitHub"
rm init.sh
