# Modern Python Project Template

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-black.json)](https://github.com/copier-org/copier)
[![Tests](https://github.com/tsvikas/python-template/actions/workflows/uv-tests.yml/badge.svg)](https://github.com/tsvikas/python-template/actions/workflows/uv-tests.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

A modern Python project template using recommended development tools and best practices.

## Features

This template provides a comprehensive set of tools to streamline your Python development workflow:

### Code Structure

- Command-line interface with [Typer](https://typer.tiangolo.com/)
- Advanced logging with [Loguru](https://loguru.readthedocs.io/)
- Modern project layout following best practices

### Development Tools

- Python dependency management with [uv](https://docs.astral.sh/uv/) (faster alternative to pip/poetry)
- Versioning management with [uv-dynamic-versioning](https://github.com/ninoseki/uv-dynamic-versioning)
- Task automation with [Just](https://just.systems/man/en/) command runner

### Code Quality

- Testing framework with [pytest](https://docs.pytest.org/)
  - Coverage reports via [pytest-coverage](https://pytest-cov.readthedocs.io/)
  - Performance benchmarking with [pytest-benchmark](https://pytest-benchmark.readthedocs.io/)
  - Additional pytest plugins for a better testing experience
- Code formatting with [Black](https://black.readthedocs.io/) or [Ruff formatter](https://docs.astral.sh/ruff/formatter/)
- Markdown formatting with [Mdformat](https://mdformat.readthedocs.io/)
- Comprehensive linting with [Ruff](https://docs.astral.sh/ruff/)
  - Replaces Flake8, isort, pyupgrade, yesqa, pycln, and dozens of plugins
- Static type checking with [MyPy](https://mypy-lang.org/)
- Spell checking with [codespell](https://github.com/codespell-project/codespell/yyzz) and [typos](https://github.com/crate-ci/typos/)

### CI/CD Integration

- Git hooks via [pre-commit](https://pre-commit.com/) with many hooks pre-configured
- Test automation with [GitHub Actions](https://docs.github.com/en/actions)
- Automated dependency updates with [Dependabot](https://docs.github.com/en/code-security/dependabot)

### Configuration Files

- [EditorConfig](https://editorconfig.org/) for consistent formatting across editors
- Comprehensive [.gitignore](https://gitignore.io/) file
- Sensible defaults for all included tools

### Documentation (Coming Soon)

- Documentation generation
- Automatic API documentation

## Getting Started

### Prerequisites

- **git**: Obviously.

- **uv**: After the template is used, this is the only requirement for development.
  Specifically, contributors to your project can use uv for building, testing, linting, and formatting.
  See the [installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

- **Copier**: For the initial creation of the project from this template, and for pulling template updates,
  you need [Copier](https://copier.readthedocs.io/)
  with the [copier_templates_extensions](https://github.com/copier-org/copier-templates-extensions) package.
  Install it with this command (requires uv):

  ```bash
  uv tool install copier --with copier_templates_extensions
  ```

- All the other developments tools are managed automatically by uv in your vertual environment,
  ensuring consistent versions across developers
  via Python's [dependency-groups](https://packaging.python.org/en/latest/specifications/dependency-groups/).

- **just**: Optional but recommended for running tasks with `just <taskname>` instead of `uv run just <taskname>`.
  See the [installation instructions](https://just.systems/man/en/packages.html).

- **gh**: GitHub CLI is not required to use this template, but it is recommended for integrating with GitHub.

### Creating a New Project

- Generate a new project with:

```bash
copier copy --trust gh:tsvikas/python-template ~/path/to/project/directory/
```

- Follow the interactive questionnaire to customize your project.
- from the project directory, run `just init` to initialize the project.

### Developing Your Project

After creating your project, run those commands from the project directory:

- Run the test suite: `just test`
- Run linting and formatting: `just lint` and `just format`, or `just check` to run them both.

See the generated `justfile` for all available commands.

## Contributing

I am exicited to see this template being used.
Feel free to suggest improvements or tell me about issues.
Contributions and Pull Requests are welcome!
