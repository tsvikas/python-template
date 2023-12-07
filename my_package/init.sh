#!/usr/bin/env bash
set -e

# git init
git init
git add --all
git reset "$0"
git commit -m "initial commit" -q

# poetry install
poetry env use python3.12
poetry install -q
git add poetry.lock
git commit -m "chore: poetry install" -q

# pre-commit update
poetry run pre-commit autoupdate -j "$(nproc)"
git add .pre-commit-config.yaml
git commit -m "chore: pre-commit update" -q

# pre-commit install
poetry run pre-commit install

echo "use 'gh repo create' to set this repo on GitHub"
echo "use 'run pre-commit install-hooks' to install the pre-commit hooks"
rm "$0"
