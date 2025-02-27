# my python copier template

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-black.json)](https://github.com/copier-org/copier)
[![Tests](https://github.com/tsvikas/python-template/actions/workflows/uv-tests.yml/badge.svg)](https://github.com/tsvikas/python-template/actions/workflows/uv-tests.yml)

## features

This is a modern python project template, aiming to use modern and recommended tools for developments.

Partial list of included tools:

### code:

- cli with [typer](https://typer.tiangolo.com/)
- logging with [loguru](https://loguru.readthedocs.io/)

### dev tools:

- python dependency management with [uv](https://docs.astral.sh/uv/)
- versioning with
  [uv-dynamic-versioning](https://github.com/ninoseki/uv-dynamic-versioning)
- task runner [just](https://just.systems/man/en/)

### code quality tools:

- testing with [pytest](https://docs.pytest.org/),
  [pytest-coverage](https://pytest-cov.readthedocs.io/),
  [pytest-benchmark](https://pytest-benchmark.readthedocs.io/),
  and more
- formatting with [black](https://black.readthedocs.io/)
  or [ruff-format](https://docs.astral.sh/ruff/formatter/)
- linting with [ruff](https://docs.astral.sh/ruff/)
- type checking with [mypy](https://mypy-lang.org/)

### ci tools:

- [pre-commit](https://pre-commit.com/)
  with many hooks pre-configured
- [github workflows](https://docs.github.com/en/actions/writing-workflows)

### other pre-set config files:

- [EditorConfig](https://editorconfig.org/)
- [gitignore](https://gitignore.io/)

### documentation generation:

WIP

## Usage

### Requirements

- To create a project from the template, you need [copier](https://copier.readthedocs.io/),
  with [copier_templates_extensions](https://github.com/copier-org/copier-templates-extensions).
  To install: `uv tool install copier --with copier_templates_extensions`

- The development requirements for the created project is only
  [uv](https://docs.astral.sh/uv/getting-started/installation/).

- Other dev-tools can be installed too, but on default they are easily managed by uv using
  python's [dependency-groups](https://packaging.python.org/en/latest/specifications/dependency-groups/).
  It is convenient to install [just](https://just.systems/man/en/packages.html),
  as it allows you to run `just <taskname>` instead of `uv run just <taskname>`

### Create a new project from the template:

Run
`copier copy gh:tsvikas/python-template ~/path/to/project/directory/`
and answer the questionnaire.
Than switch to the newly created directory and run `just init`

### Developing your project

WIP
