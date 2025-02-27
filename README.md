# my python copier template
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-black.json)](https://github.com/copier-org/copier)

including:

- code:
  - cli with [typer](https://typer.tiangolo.com/)
  - logging with [loguru](https://loguru.readthedocs.io/)
- dev tools:
  - python dependency management with [uv](https://docs.astral.sh/uv/)
  - versioning with
    [uv-dynamic-versioning](https://github.com/ninoseki/uv-dynamic-versioning)
  - task runner [just](https://just.systems/man/en/)
- code quality tools:
  - testing with [pytest](https://docs.pytest.org/),
    [pytest-coverage](https://pytest-cov.readthedocs.io/),
    [pytest-benchmark](https://pytest-benchmark.readthedocs.io/),
    and more
  - formatting with [black](https://black.readthedocs.io/)
    or [ruff-format](https://docs.astral.sh/ruff/formatter/)
  - linting with [ruff](https://docs.astral.sh/ruff/)
  - type checking with [mypy](https://mypy-lang.org/)
- ci:
  - [pre-commit](https://pre-commit.com/)
    with many hooks pre-configured
  - [github workflows](https://docs.github.com/en/actions/writing-workflows)
- pre-set config files:
  - [EditorConfig](https://editorconfig.org/)
  - [gitignore](https://gitignore.io/)
- documentation generation: WIP

## Usage

To use:

```
copier copy <src> ~/code/my-repo
~/code/my-repo/init.sh
```

or:

```
copier copy gh:tsvikas/python-template ~/code/my-repo
~/code/my-repo/init.sh
```
