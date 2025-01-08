#!/usr/bin/env python3
import argparse
import shutil
import sys
from pathlib import Path

SOURCE_DIRECTORY = Path(__file__).parent / "project_name"


def copy_package(dst: Path, package_name: Path, todo_folder: Path | None = None):
    # copy the project to the destination
    shutil.copytree(SOURCE_DIRECTORY, dst, ignore=shutil.ignore_patterns(".*cache"))

    # rename
    package_template = "{{package_name}}"
    project_template = "{{project_name}}"
    project_name = dst.name
    # foldwrs
    dst.joinpath(package_template).rename(dst.joinpath(package_name))
    # file contents
    for file in dst.rglob("*"):
        if file.is_file():
            file_contents = file.read_text()
            file_contents = file_contents.replace(package_template, package_name)
            file_contents = file_contents.replace(project_template, project_name)
            file_contents = file_contents.replace("{{python_minor}}", "12")
            file.write_text(file_contents)

    # create the TODO.md link
    if todo_folder:
        link_src = dst.joinpath("TODO.md")
        link_dst = todo_folder.joinpath(dst.name).with_suffix(".md").resolve()
        if link_dst.exists():
            print(
                f"can't create a TODO.md file in {link_src} because {link_dst} exists)"
            )
        else:
            link_src.symlink_to(link_dst)


def parse_args() -> tuple[Path, str, Path | None]:
    parser = argparse.ArgumentParser(
        prog="create-python-package",
        description="Create a new python project using the python package",
    )
    parser.add_argument(
        "destination",
        help="The destination directory to create the package in",
    )
    parser.add_argument(
        "-p",
        "--package_name",
        default=None,
        help="The name of the package. Must be a valid identifier. "
        "Automatically derived from the destination.",
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
    package_name = args.package_name or destination.name.replace("-", "_")
    if not package_name.isidentifier():
        print(f"Invalid package name: {package_name}")
        sys.exit(2)
    todo_folder = Path(args.todo_folder).expanduser() if args.todo_folder else None
    if todo_folder and not todo_folder.exists():
        print(f"TODO folder doesn't exist: {todo_folder}")
        sys.exit(3)
    return destination, package_name, todo_folder


def main():
    destination, package_name, todo_folder = parse_args()
    copy_package(destination, package_name, todo_folder)

    # print instructions
    print(f"the python project is in {destination}")
    print(
        "modify any file you need to modify, "
        "and use `init.sh` to initialize the project"
    )


if __name__ == "__main__":
    main()
