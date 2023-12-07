#!/usr/bin/env bash
set -e

# git init
git init
git add --all
git reset "$0"
git commit -m "initial commit"

# poetry install
poetry env use python3.12
poetry install -q
git add poetry.lock
git commit -m "chore: poetry install"

# pre-commit update
poetry run pre-commit autoupdate
git add .pre-commit-config.yaml
git commit -m "chore: pre-commit update"

# pre-commit install
poetry run pre-commit install

echo "use 'gh repo create' to set this repo on GitHub"
rm "$0"
