default:
  @just --list

check:
  pre-commit run --all-files
  just test

test:
  rm -rf .ctt
  uvx --from copier-template-tester --with copier_templates_extensions ctt

# add a new version tag and push it
tag version commit="HEAD": check
  # TODO: check the commit and not the current state.
  git tag -a v{{ version }} -m "Release v{{ version }}" {{ commit }}
  git push --tags
