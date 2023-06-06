#!/usr/bin/env python3
import argparse
import subprocess


def diff_summary(commit_1, commit_2, diff_cmd="diff"):
    subprocess.run(
        [
            "fish",
            "-c",
            (
                f"{diff_cmd}"
                f" (scripts/summarize_dvc_lock.py -c {commit_1} | psub)"
                f" (scripts/summarize_dvc_lock.py -c {commit_2} | psub)"
            ),
        ]
    )


def diff_file(filename, commit_1, commit_2, diff_cmd="diff"):
    subprocess.run(
        [
            "fish",
            "-c",
            (
                f"{diff_cmd}"
                f" (scripts/dvc_show.py {filename} -c {commit_1} | psub)"
                f" (scripts/dvc_show.py {filename} -c {commit_2} | psub)"
            ),
        ]
    )


def main():
    parser = argparse.ArgumentParser(
        prog="dvc_diff",
        description="show diff of dvc.lock or specific file",
    )
    parser.add_argument("--filename", "-f")
    parser.add_argument("--meld", action="store_true")
    parser.add_argument("commit_1")
    parser.add_argument("commit_2")
    args = parser.parse_args()
    diff_cmd = "meld" if args.meld else "diff"
    if args.filename is None:
        diff_summary(args.commit_1, args.commit_2, diff_cmd)
    else:
        diff_file(args.filename, args.commit_1, args.commit_2, diff_cmd)


if __name__ == "__main__":
    main()
