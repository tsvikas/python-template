#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

import yaml


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


def find_file_hash(lock_data: dict, filename: str):
    for _stage_name, stage in lock_data["stages"].items():
        for file_values in stage["deps"] + stage["outs"]:
            if file_values["path"] == filename:
                return file_values["md5"]
    raise RuntimeError("File not found in dvc.lock")


def read_file(commit, filename):
    lock_data = get_lock_data(commit)
    filehash = find_file_hash(lock_data, filename)
    file_path = find_dvc_basedir() / ".dvc/cache" / filehash[:2] / filehash[2:]
    return file_path.read_text()


def main():
    parser = argparse.ArgumentParser(
        prog="dvc_show",
        description="show file from dvc commit",
    )
    parser.add_argument("filename")
    parser.add_argument("--commit", "-c")
    args = parser.parse_args()
    file_content = read_file(args.commit, args.filename)
    print(file_content)


if __name__ == "__main__":
    main()
