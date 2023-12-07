#!/usr/bin/env python3
import argparse
import shutil
import sys
from pathlib import Path

SOURCE_DIRECTORY = Path(__file__).parent / "my_package"


def main():
    parser = argparse.ArgumentParser(
        prog="create-python-package",
        description="Create a new python project using the python package",
    )
    parser.add_argument(
        "destination",
        help="The destination directory to create the package in. the last part of the path will be the package name",
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

    # copy to the destination
    shutil.copytree(SOURCE_DIRECTORY, destination, ignore=shutil.ignore_patterns(".*cache"))

    # rename file contents from "my_package" to the package name
    destination.joinpath("my_package").rename(destination.joinpath(package_name))
    for file in destination.rglob("*"):
        if file.is_file():
            file_contents = file.read_text()
            file_contents = file_contents.replace("my_package", package_name)
            file.write_text(file_contents)

    # print instructions
    print(f"the python project is in {destination}")
    print(
        "modify any file you need to modify, "
        "and use `init.sh` to initialize the project"
    )


if __name__ == "__main__":
    main()
