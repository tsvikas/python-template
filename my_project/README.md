{{my_project}}
================
## Usage
```
import {{my_package}}
```

## Development
* install git, python3.{{python_minor}}, {{manager}} {%- if ci == "poe" %}, poethepoet {%- endif %}.
* git clone this repo
* create a venv using {% if manager=="poetry" -%}
  `poetry env use python3.{{python_minor}}; poetry install`
  {%- elif manager=="uv" -%}
  `uv python pin python3.{{python_minor}}; uv sync`
  {%- endif %}
* enable pre-commit checks with `{{manager}} run pre-commit install`

## Code quality
{%- if ci == "poe" %}
* use `poe check` to verify code quality
{%- else %}
* use `{{manager}} run ruff check .` to verify code quality
* use `{{manager}} run mypy` to verify check typing
{%- if use_ruff_format %}
* use `{{manager}} run ruff format .` {% endif %} to format code and docs
{%- else %}
* use `{{manager}} run black .` {% endif %} to format code
* use `git ls-files -z -- '*.md' '*.rst' '*.tex' '*.py' | xargs -0 blacken-docs` to format docs
{%- endif %}
* use `{{manager}} run pytest` to run tests
{%- endif %}

## Build
{%- if ci == "poe" %}
* use `poe version` to see the current version
* use `poe tag vX.Y.Z` to add a git tag
{%- else %}
* run formatting, linting, and tests.
* use `{{manager}} run dunamai from git` to see the current version
* use `git tag -a vX.Y.Z -m "version vX.Y.Z" -e` to add a git tag
{%- endif %}
* use `{{manager}} build` to build
* push the tag with `git push origin tag vX.Y.Z`
