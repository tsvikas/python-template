{{my_project}}
================
## Usage
```
import {{my_package}}
```

## Development
* install git, python3.{{python_minor}}, {{manager}}, poethepoet.
* git clone this repo
* create a venv using {% if manager=="poetry" -%}
  `poetry env use python3.{{python_minor}}; poetry install`
  {%- elif manager=="uv" -%}
  `uv python pin python3.{{python_minor}}; uv sync`
  {%- endif %}
* enable pre-commit checks with `{{manager}} run pre-commit install`
* use `poe check` to verify code quality

## Build
* use `poe version` to see the current version
* use `poe tag vX.Y.Z` to add a git tag. you still need to push it.
* use `{{manager}} build` to build
