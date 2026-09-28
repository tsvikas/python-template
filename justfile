list-tasks:
  @just --list

prepare:
    uv run prek install

check: lint test

lint:
  uv run prek run --all-files

test:
  rm -rf .ctt
  # ctt renders from a copy under $TMPDIR, and the generated `just init` runs
  # detect-secrets before ctt normalizes `_src_path`. macOS's per-user $TMPDIR
  # (/var/folders/xx/<random>/T) reads as a high-entropy secret, so use /tmp.
  TMPDIR=/tmp uv run ctt

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
  uv run prek update -j "$( (uname -s | grep -q Linux && nproc) || (uname -s | grep -q Darwin && sysctl -n hw.ncpu) || echo 1 )"
  uvx sync-pre-commit-deps --yaml-mapping 2 --yaml-sequence 4 --yaml-offset 2 .pre-commit-config.yaml || { \
    echo "Note: '.pre-commit-config.yaml' changed, and might lost its formatting." \
    && exit 1; \
  }

# Field-test the deps-update workflow of a template branch on GitHub: render it into a
# throwaway repo (force-pushed, so never point this at a real one) with stale dependencies
field-test-deps-update ref=`git branch --show-current` repo=("tsvikas/" + file_name(justfile_directory()) + "-sandbox"):
  #!/usr/bin/env bash
  set -euo pipefail
  dir=$(mktemp -d /tmp/field-test.XXXXXX)  # /tmp, for the reason in `test`
  uvx copier copy --defaults --vcs-ref "{{ ref }}" \
    -d user_name="Marty McFly" -d user_email=marty.mcfly@example.com \
    -d github_user="$(dirname "{{ repo }}")" -d project_name="$(basename "{{ repo }}")" \
    -d package_description="Field test for python-template." \
    -d in_rtd=true -d cli_framework=cyclopts \
    . "$dir"
  cd "$dir"
  git init -q -b main
  TMPDIR=/tmp VIRTUAL_ENV='' uv run just init
  # Versions with known advisories, and an old hook, so there are updates and findings
  VIRTUAL_ENV='' uv lock -P jinja2==3.1.4 -P requests==2.31.0 -P urllib3==2.2.1 -P idna==3.6
  sed -i.bak '/codespell-project/{n;s/rev: .*/rev: v2.4.1/;}' .pre-commit-config.yaml && rm .pre-commit-config.yaml.bak
  git commit -qam "🧪 Make dependencies stale for the field test"
  # A branch that leaves uv.lock alone, where CI should skip the audit
  git switch -qc field-test/no-lock-change
  printf "\nField test branch.\n" >> README.md
  VIRTUAL_ENV='' uv run prek run --files README.md > /dev/null || true  # let the formatters settle it
  git commit -qam "📝 Touch the README only"
  git switch -q main

  gh repo view "{{ repo }}" > /dev/null 2>&1 || gh repo create "{{ repo }}" --private
  # "Allow GitHub Actions to create and approve pull requests", which deps-update needs
  gh api -X PUT "repos/{{ repo }}/actions/permissions/workflow" \
    -f default_workflow_permissions=read -F can_approve_pull_request_reviews=true
  for pr in deps/update field-test/no-lock-change; do
    gh pr close "$pr" --repo "{{ repo }}" --delete-branch 2> /dev/null || true
  done
  git push -q --force "git@github.com:{{ repo }}.git" main field-test/no-lock-change

  # Just-pushed workflows take a moment to register
  until gh workflow run deps-update.yml --repo "{{ repo }}" 2> /dev/null; do sleep 5; done
  # Only now, since a pull request opened before the workflows register gets no CI
  gh pr create --repo "{{ repo }}" --head field-test/no-lock-change --base main \
    --title "📝 Touch the README only" --body "Field test: CI should skip pip-audit here."
  sleep 5
  run=$(gh run list --repo "{{ repo }}" --workflow deps-update.yml --limit 1 --json databaseId -q '.[0].databaseId')
  gh run watch "$run" --repo "{{ repo }}" --exit-status > /dev/null
  echo "deps PR: $(gh pr view deps/update --repo "{{ repo }}" --json url -q .url)"
  echo "Its CI runs next; watch it with: gh run list --repo {{ repo }}"
