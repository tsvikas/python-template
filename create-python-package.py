#!/usr/bin/env python3
import argparse
import shutil
import sys
from pathlib import Path

SOURCE_DIRECTORY = Path(__file__).parent / "my_package"


def copy_package(dst: Path, todo_folder: Path | None = None):
    template_name = "my_package"
    package_name = dst.name

    # copy to the destination
    shutil.copytree(SOURCE_DIRECTORY, dst, ignore=shutil.ignore_patterns(".*cache"))
    if todo_folder:
        link_src = dst.joinpath("TODO.md")
        link_dst = todo_folder.joinpath(package_name).with_suffix(".md").resolve()
        if link_dst.exists():
            print(
                f"can't create a TODO.md file in {link_src} because {link_dst} exists)"
            )
        else:
            link_src.symlink_to(link_dst)

    # rename file contents from "my_package" to the package name
    dst.joinpath(template_name).rename(dst.joinpath(package_name))
    for file in dst.rglob("*"):
        if file.is_file():
            file_contents = file.read_text()
            file_contents = file_contents.replace(template_name, package_name)
            file.write_text(file_contents)


def parse_args() -> Path:
    parser = argparse.ArgumentParser(
        prog="create-python-package",
        description="Create a new python project using the python package",
    )
    parser.add_argument(
        "destination",
        help="The destination directory to create the package in. the last part of the path will be the package name",
    )
    parser.add_argument(
        "-t",
        "--todo-folder",
        default="~/code_TODOs",
        help="Create a todo file in this folder, and link into it",
    )
    args = parser.parse_args()
    # check the arguments
    destination = Path(args.destination)
    if destination.exists():
        print(f"Destination already exists: {destination}")
        sys.exit(1)
    package_name = destination.name
    if not package_name.isidentifier():
        print(f"Invalid package name: {package_name}")
        sys.exit(2)
    todo_folder = Path(args.todo_folder).expanduser() if args.todo_folder else None
    if todo_folder and not todo_folder.exists():
        print(f"TODO folder doesn't exist: {todo_folder}")
        sys.exit(3)
    return destination, todo_folder


def main():
    destination, todo_folder = parse_args()
    copy_package(destination, todo_folder)

    # print instructions
    print(f"the python project is in {destination}")
    print(
        "modify any file you need to modify, "
        "and use `init.sh` to initialize the project"
    )


if __name__ == "__main__":
    main()
