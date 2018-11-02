# encoding: utf-8

import importlib
import logging
import typing
from collections import UserList
from pathlib import Path

FORBIDDEN_EXTENSIONS = {'.pyc', '.log', '.ini', '.DS_Store', '.db'}
FORBIDDEN_NAMES = {'__pycache__'}


def transform_path(path: typing.Union[Path, str]) -> str:
    return str(path).replace('/', '.').replace('.py', '')


def filter_path(path: typing.Union[Path, str]) -> bool:
    string_path = str(path)

    if any(string_path.endswith(ext) for ext in FORBIDDEN_EXTENSIONS):
        return False

    if string_path in FORBIDDEN_NAMES:
        return False

    return True


class LoadList(UserList):
    """A class that encompasses behavior related to discovering extensions and loading them."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = logging.getLogger(__name__)

    def build(self, exts_path: Path):
        if not exts_path.is_dir():
            self.log.warning('Cannot build load list: %s is not a directory.', exts_path)
            return

        # Build a list of extensions to load.
        paths = [
            transform_path(path)
            for path in exts_path.iterdir()
            if filter_path(path)
        ]

        def ext_filter(path: str) -> bool:
            try:
                module = importlib.import_module(path)
                return hasattr(module, 'setup')
            except Exception:
                # Failed to import, extension might be bugged.
                # If this extension was previously included, retain it in the
                # load list because it might be fixed and reloaded later.
                #
                # Otherwise, discard.
                previously_included = path in self.data
                if not previously_included:
                    self.log.exception('Excluding %s from the load list:', path)
                else:
                    self.log.warning(
                        ('%s has failed to load, but it will be retained in '
                         'the load list because it was previously included.'),
                        path,
                    )
                return previously_included

        self.data = list(filter(ext_filter, paths))
