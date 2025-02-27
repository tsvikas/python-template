default:
  @just --list

test:
  pre-commit run --all-files
  rm -rf .ctt
  uvx --from copier-template-tester --with copier_templates_extensions ctt
