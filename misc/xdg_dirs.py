"""set BASE_DIR with locations for program files."""

from pathlib import Path

import xdg_base_dirs


class XDGPaths:
    """Get paths, according to the XDG Base Directory Specification.

    https://specifications.freedesktop.org/basedir-spec/latest/
    """

    def __init__(self, prog_name: str):
        """Get paths for a program, according to the XDG Base Directory Specification.

        all paths are in a subdir `prog_name`
        """
        self.prog_name = prog_name

    def existing_data_files(self, filename: str) -> list[Path]:
        """Get 'prog_name/filename' from '$XDG_DATA_HOME' and '$XDG_DATA_DIRS'.

        Those are the directories in which data files should be stored.
        """
        return [
            fn
            for d in [xdg_base_dirs.xdg_data_home(), *xdg_base_dirs.xdg_data_dirs()]
            if (fn := d / self.prog_name / filename).exists()
        ]

    def existing_config_files(self, filename: str) -> list[Path]:
        """Get 'prog_name/filename' from '$XDG_CONFIG_HOME' and '$XDG_CONFIG_DIRS'.

        Those are the directories in which configuration files should be stored.
        """
        return [
            fn
            for d in [xdg_base_dirs.xdg_config_home(), *xdg_base_dirs.xdg_config_dirs()]
            if (fn := d / self.prog_name / filename).exists()
        ]

    def data_file(self, filename: str) -> Path:
        """Get '$XDG_DATA_HOME/prog_name/filename'.

        '$XDG_DATA_HOME/prog_name' is the directory to which
        user-specific data files should be stored.
        """
        return xdg_base_dirs.xdg_data_home() / self.prog_name / filename

    def config_file(self, filename: str) -> Path:
        """Get '$XDG_CONFIG_HOME/prog_name/filename'.

        '$XDG_CONFIG_HOME/prog_name' is the directory to which
        user-specific configuration files should be stored.
        """
        return xdg_base_dirs.xdg_config_home() / self.prog_name / filename

    def state_file(self, filename: str) -> Path:
        """Get '$XDG_STATE_HOME/prog_name/filename'.

        '$XDG_STATE_HOME/prog_name' is the directory to which
        user-specific state files should be stored.

        It should contain state data that should persist between (application)
        restarts, but that is not important or portable enough to the user that
        it should be stored in $XDG_DATA_HOME. It may contain:
        * actions history (logs, history, recently used files, …)
        * current state of the application that can be reused on a restart
          (view, layout, open files, undo history, …)
        """
        return xdg_base_dirs.xdg_state_home() / self.prog_name / filename

    def cache_file(self, filename: str) -> Path:
        """Get '$XDG_CACHE_HOME/prog_name/filename'.

        '$XDG_CACHE_HOME/prog_name' is the directory to which
        user-specific non-essential (cached) data files should be stored.
        """
        return xdg_base_dirs.xdg_cache_home() / self.prog_name / filename

    def runtime_file(self, filename: str) -> Path:
        """Get '$XDG_RUNTIME_DIR/prog_name/filename'.

        '$XDG_RUNTIME_DIR/prog_name' is the directory to which
        user-specific runtime files and other file objects should be placed.
        """
        return xdg_base_dirs.xdg_runtime_dir() / self.prog_name / filename


BASE_DIRS = XDGPaths(prog_name="TODO: CHANGE ME")
