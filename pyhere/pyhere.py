# -*- coding: utf-8 -*-

import sys

if sys.version_info[0] == 2:
    from pathlib2 import Path
else:
    from pathlib import Path

import warnings

class RootIndicatorException(Exception):
    pass

DEFAULT_ROOT_INDICATORS = [
    ".here",
    "requirements.txt",
    "setup.py",
    ".vscode", # vscode project
    ".idea", # pycharm project
    ".git",
    ".spyderproject", # spyder
    ".spyproject", # spyder
    ".ropeproject" # rope
]

def here(*args, root_indicators=None):
    """
    Finds a project's root directory and then iteratively appends all passed
    arguments to it, construction a path relative to the root directory.

    Parameters
    ----------
    *args : Path or str
        The path additions to be attached to the root directory.
    **kwargs: 
        root_indicators: list of strings of possible root indicators. If not set,
        DEFAULT_ROOT_INDICATORS are used.


    Returns
    -------
    Path
        A path directory pointing to the passed arguments relative to the
        project's root directory.

    """
    heredir = find_root(root_indicators=root_indicators)
    
    for arg in args:
        heredir = heredir / arg
      
    return heredir

def set_here(wd = None):
    """
    Creates a .here file at the passed directory.

    Parameters
    ----------
    wd : Path object or string
        The directory that a .here file will be created in. If none is set,
        uses Path.cwd()
    
    """
    if wd is None:
        wd = Path.cwd()
    elif type(wd) is str:
        wd = Path(wd)

    wd.parent.mkdir(parents=True, exist_ok=True)
    wd.joinpath(".here").touch()
        
    
def find_root(path = None, root_indicators=None):
    """
    Find's the root of a python project.
    
    Traverses directories upwards, iteratively searching for root_indicators.
    If no match is found, the system root is returned and a warning is thrown.

    Parameters
    ----------
    path : Path, str or None
        The starting directory to begin the search. If none is set, uses
        Path.cwd()
    root_indicators: str or list of string giving root indicators. If None,
        use DEFAULT_ROOT_INDICATORS

    Returns
    -------
    Path
        Either the path where a root_indicator was found or the system root.

    """
    if root_indicators is None:
        root_indicators = DEFAULT_ROOT_INDICATORS
    elif isinstance(root_indicators, str):
        root_indicators = [root_indicators]
    elif isinstance(root_indicators,(list, tuple, set)):
        try:
            assert len(root_indicators) > 0
            assert all([isinstance(root,str) for root in root_indicators])
        except AssertionError as exc:
            raise RootIndicatorException("Unrecognized root indicator sequence") from exc
    else:
        raise RootIndicatorException(f"Unreocgnizesd root indicator {root_indicators}")
    if path is None:
        return find_root(Path.cwd(), root_indicators=root_indicators)
    else:
        for root_indicator in root_indicators:
            if path.joinpath(root_indicator).exists():
                return path.resolve()
        
        next_path = path / ".."
        
        # if we've hit the system root
        if (next_path.resolve() != path.resolve()):
            return find_root(next_path, root_indicators=root_indicator)
        else:
            warnings.warn(
                "No project indicator found - returning root system directory"
            )
            return path.resolve()
