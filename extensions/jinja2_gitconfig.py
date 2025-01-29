import re

from jinja2 import Environment
from jinja2.ext import Extension


def is_valid_git_config(s: str) -> bool:
    pattern = r"[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+"
    return bool(re.fullmatch(pattern, s))


def git_config(key: str) -> str:
    """Get a git config value

    Parameters
    ----------
    key : str
        The config key to get.

    Returns
    -------
    str
        The value of git config <key>.

    """
    import subprocess  # nosec

    if not is_valid_git_config(key):
        raise ValueError(f"{key!r} is not a valid git config value")

    process = subprocess.run(  # nosec
        ["/usr/bin/git", "config", key],
        capture_output=True,
        text=True,
        check=False,
    )  # nosec
    return process.stdout.rstrip()


class GitConfigExtension(Extension):
    def __init__(self, environment: Environment) -> None:
        super().__init__(environment)
        environment.filters["git_config"] = git_config
