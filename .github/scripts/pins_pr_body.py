"""Write the body of the template action pins PR, with the release notes of each bump.

Reads the pin changes from `git diff` of the template's workflows, and fetches the
notes of every release in each bumped range with `gh`. Prints the body to stdout.
"""

import json
import re
import subprocess
import sys

WORKFLOWS = "project_name/.github/workflows"
# `-      - uses: owner/repo/optional/path@<sha> # v1.2.3`
PIN = re.compile(
    r"^(?P<sign>[-+])\s*(?:-\s+)?uses:\s*(?P<repo>[\w.-]+/[\w.-]+)\S*@[0-9a-f]{40}"
    r"\s*#\s*(?P<version>\S+)"
)
# GitHub rejects PR bodies over 65536 characters.
MAX_NOTES = 5_000
MAX_BODY = 60_000

# One line per paragraph, since GitHub renders line breaks inside a paragraph.
INTRO = (
    "Automated update of the SHA-pinned actions under"
    " `project_name/.github/workflows/`, which Dependabot cannot reach."
    " Each pin is moved to the latest release"
    " and its `# vX.Y.Z` comment is rewritten to match.\n"
    "\n"
    "Review the diff as you would a Dependabot PR:"
    " check the release notes below for anything behavioural,"
    " especially on major bumps.\n"
)


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(n) for n in re.findall(r"\d+", version))


def quote_notes(notes: str, repo: str) -> str:
    """Quote upstream notes so that they neither notify nor cross-reference upstream.

    As Dependabot does: `redirect.github.com` links create no "mentioned this"
    backlinks, bare `#123` would otherwise point at this repo, and `@user` in a code
    span pings no one.
    """
    notes = notes.replace("https://github.com/", "https://redirect.github.com/")
    notes = re.sub(
        r"(?<![\w/`\[&])#(\d+)\b",
        rf"[#\1](https://redirect.github.com/{repo}/issues/\1)",
        notes,
    )
    notes = re.sub(r"(?<![\w`/])@([A-Za-z0-9][\w-]*(?:/[\w.-]+)?)", r"`@\1`", notes)
    return "\n".join(f"> {line}".rstrip() for line in notes.splitlines())


def gh(*args: str) -> str:
    return subprocess.run(
        ["gh", *args], capture_output=True, text=True, check=True
    ).stdout


def pin_changes() -> dict[str, tuple[str, str]]:
    """Map each bumped `owner/repo` to its (oldest old, newest new) version."""
    diff = subprocess.run(
        ["git", "diff", "-U0", "--", WORKFLOWS],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    versions: dict[str, dict[str, set[str]]] = {}
    for line in diff.splitlines():
        if m := PIN.match(line):
            by_sign = versions.setdefault(m["repo"], {"-": set(), "+": set()})
            by_sign[m["sign"]].add(m["version"])
    return {
        repo: (min(v["-"], key=version_key), max(v["+"], key=version_key))
        for repo, v in sorted(versions.items())
        if v["-"] and v["+"] and v["-"] != v["+"]
    }


def release_notes(repo: str, old: str, new: str) -> str:
    """The notes of every stable release of `repo` after `old`, up to `new`."""
    releases = json.loads(
        gh(
            "release",
            "list",
            "-R",
            repo,
            "-L",
            "100",
            "--exclude-drafts",
            "--exclude-pre-releases",
            "--json",
            "tagName",
        )
    )
    lo, hi = version_key(old), version_key(new)
    tags = sorted(
        (r["tagName"] for r in releases if lo < version_key(r["tagName"]) <= hi),
        key=version_key,
        reverse=True,
    )
    sections = []
    for tag in tags:
        release = json.loads(
            gh("release", "view", tag, "-R", repo, "--json", "body,url")
        )
        notes = release["body"].strip() or "_No release notes._"
        if len(notes) > MAX_NOTES:
            notes = (
                notes[:MAX_NOTES]
                + f"\n\n… truncated, see [the release]({release['url']})."
            )
        notes = quote_notes(notes, repo)
        sections.append(f"### [{tag}]({release['url']})\n\n{notes}\n")
    if not sections:
        sections.append(f"No releases found between `{old}` and `{new}`.\n")
    compare = f"https://github.com/{repo}/compare/{old}...{new}"
    return (
        f"<details>\n<summary>{repo} {old} → {new}</summary>\n\n"
        f"[Compare {old}...{new}]({compare})\n\n"
        + "\n".join(sections)
        + "\n</details>\n"
    )


def main() -> None:
    body = INTRO + "\n## Release notes\n\n"
    for repo, (old, new) in pin_changes().items():
        try:
            section = release_notes(repo, old, new)
        except subprocess.CalledProcessError as exc:
            print(f"{repo}: {exc.stderr}", file=sys.stderr)
            section = f"- {repo} {old} → {new}: could not fetch the release notes.\n"
        if len(body) + len(section) > MAX_BODY:
            section = (
                f"- {repo} {old} → {new}: omitted, the PR body is at its size limit.\n"
            )
        body += section
    print(body)


if __name__ == "__main__":
    main()
