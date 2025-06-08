default:
  @just --list

check:
  pre-commit run --all-files
  just test

test:
  rm -rf .ctt
  uv run ctt

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
update-deps:
  pre-commit autoupdate -j "$( (uname -s | grep -q Linux && nproc) || (uname -s | grep -q Darwin && sysctl -n hw.ncpu) || echo 1 )"
  pre-commit run -a sync-pre-commit-deps
