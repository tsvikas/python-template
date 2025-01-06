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
{%- endif %}

## Build
{%- if ci == "poe" %}
* use `poe version` to see the current version
* use `poe tag vX.Y.Z` to add a git tag
{%- endif %}
* use `{{manager}} build` to build
* push the tag with `git push origin tag vX.Y.Z`
