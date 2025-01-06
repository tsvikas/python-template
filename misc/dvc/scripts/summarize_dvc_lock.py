#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

import yaml


def add_dot(file_name):
    if "/" not in file_name:
        file_name = "./" + file_name
    if file_name[-1] != "/" and "." not in file_name:
        print(file_name, "needs / at end?")
    return file_name


def summarize_lock_file(lock_data: dict):
    file_hashes = {}
    dep_files = set()
    out_files = set()
    for _stage_name, stage in lock_data["stages"].items():
        for file_values in stage["deps"]:
            file_name = add_dot(file_values["path"])
            dep_files.add(file_name)
            file_hashes[file_name] = file_values["md5"]
        for file_values in stage["outs"]:
            file_name = add_dot(file_values["path"])
            out_files.add(file_name)
            file_hashes[file_name] = file_values["md5"]
    file_hashes = {k: file_hashes[k] for k in sorted(file_hashes)}
    # find mid_files
    mid_files = dep_files.intersection(out_files)
    dep_files = dep_files - mid_files
    out_files = out_files - mid_files
    return {
        "dep": {fn: file_hashes[fn] for fn in sorted(dep_files)},
        "mid": {fn: file_hashes[fn] for fn in sorted(mid_files)},
        "out": {fn: file_hashes[fn] for fn in sorted(out_files)},
    }


def find_dvc_basedir():
    base_dir = Path().resolve()
    while not base_dir.joinpath("dvc.lock").exists():
        if base_dir == Path("/"):
            raise RuntimeError("dvc.lock file not found")
        base_dir = base_dir.parent
    return base_dir


def get_lock_data(commit=None):
    if commit is None:
        lock_file = find_dvc_basedir() / "dvc.lock"
        assert lock_file.exists()
        with lock_file.open() as f:
            return yaml.safe_load(f)
    else:
        ret = subprocess.run(
            ["git", "show", f"{commit}:dvc.lock"], capture_output=True, check=True
        )
        return yaml.safe_load(ret.stdout)


def main():
    parser = argparse.ArgumentParser(
        prog="summarize_dvc_lock",
        description="make shorter dvc.lock representation",
    )
    parser.add_argument("--commit", "-c")
    args = parser.parse_args()
    lock_data = get_lock_data(args.commit)
    summary = summarize_lock_file(lock_data)
    print(yaml.safe_dump(summary, sort_keys=False))


if __name__ == "__main__":
    main()
