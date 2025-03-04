default:
  @just --list

check:
  pre-commit run --all-files
  just test

test:
  rm -rf .ctt
  uvx --from copier-template-tester --with copier_templates_extensions ctt
