default:
  @just --list

check: lint test

lint:
  pre-commit run --all-files

test:
  rm -rf .ctt
  uv run ctt

_assert_clean_repo:
  [ -z "$(git status --porcelain)" ]

# Check the code, and push if it pass
check-and-push: _assert_clean_repo check
  git push --follow-tags

# add a new version tag and push it
tag version commit="HEAD": (_assert-legal-version version)
  just check-at-commit {{ commit }}
  just tag-skip-check {{ version }} {{ commit }}

_assert-legal-version version:
  @echo "{{ version }}" | grep -q '^[0-9]' || ( echo "Error: version name should start with a digit" && false )

tmp_rc_dir := '/tmp/rc/' + file_name(justfile_directory()) + '/' + datetime('%s')

check-at-commit commit:
  git worktree add {{ tmp_rc_dir }} --detach {{ commit }}
  just -f {{ tmp_rc_dir }}/justfile check || ( git worktree remove -f {{ tmp_rc_dir }} && false )
  git worktree remove -f {{ tmp_rc_dir }}

tag-skip-check version commit: (_assert-legal-version version)
  git tag -a v{{ version }} -m "Release v{{ version }}" {{ commit }}
  git push --tags

# Update all dependencies
deps-update:
  uv sync --upgrade
  uv run pre-commit autoupdate -j "$( (uname -s | grep -q Linux && nproc) || (uname -s | grep -q Darwin && sysctl -n hw.ncpu) || echo 1 )"
  uvx sync-pre-commit-deps --yaml-mapping 2 --yaml-sequence 4 --yaml-offset 2 .pre-commit-config.yaml || { \
    echo "Note: '.pre-commit-config.yaml' changed, and might lost its formatting." \
    && exit 0; \
  }
