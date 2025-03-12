default:
  @just --list

check:
  pre-commit run --all-files
  just test

test:
  rm -rf .ctt
  uvx --from copier-template-tester --with copier_templates_extensions ctt

tmp_rc_dir := '/tmp/rc/' + file_name(justfile_directory()) + '/' + datetime('%s')

# add a new version tag and push it
tag version commit="HEAD":
  echo {{ tmp_rc_dir }}
  echo "{{ version }}" | grep -q '^[0-9]'
  git worktree add --detach {{ tmp_rc_dir }} {{ commit }}
  just -f {{ tmp_rc_dir }}/justfile check
  git worktree remove {{ tmp_rc_dir }}
  git tag -a v{{ version }} -m "Release v{{ version }}" {{ commit }}
  git push --tags
