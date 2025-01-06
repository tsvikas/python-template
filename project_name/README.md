{{project_name}}
================
## Usage
```
import {{package_name}}
```

## Development
* install git, python3.{{python_minor}}, uv {%- if ci == "poe" %}, poethepoet {%- endif %}.
* git clone this repo
* create a venv using `uv python pin python3.{{python_minor}}; uv sync`
* enable pre-commit checks with `uv run pre-commit install`

## Code quality
{%- if ci == "poe" %}
* use `poe check` to verify code quality
{%- else %}
* use `uv run ruff check .` to verify code quality
* use `uv run mypy` to verify check typing
{%- if use_ruff_format %}
* use `uv run ruff format .` to format code and docs
{%- else %}
* use `uv run black .` to format code
* use `git ls-files -z -- '*.md' '*.rst' '*.tex' '*.py' | xargs -0 blacken-docs` to format docs
{%- endif %}
* use `uv run pytest` to run tests
{%- endif %}

## Build
{%- if ci == "poe" %}
* use `poe version` to see the current version
* use `poe tag vX.Y.Z` to add a git tag
{%- else %}
* run formatting, linting, and tests.
* use `uv run dunamai from git` to see the current version
* use `git tag -a vX.Y.Z -m "version vX.Y.Z" -e` to add a git tag
{%- endif %}
* use `uv build` to build
* push the tag with `git push origin tag vX.Y.Z`
