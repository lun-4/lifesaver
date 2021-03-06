# encoding: utf-8

import asyncio
import json
import os
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, Type


class AsyncStorage(ABC):
    @abstractmethod
    async def put(self, key: str, value: Any):
        """Put a value into storage."""
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str):
        """Return a value from storage."""


class AsyncJSONStorage(AsyncStorage):
    """
    Asynchronous JSON file based storage.

    Based off of RoboDanny's excellent config.py::

        https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/utils/config.py
    """

    def __init__(
        self,
        file: str,
        *,
        encoder: Type[json.JSONEncoder] = json.JSONEncoder,
        object_hook=None,
        loop: asyncio.AbstractEventLoop = None,
    ) -> None:
        self.file = file
        self._data: Dict[str, Any] = {}
        self.loop = loop or asyncio.get_event_loop()
        self.lock = asyncio.Lock()
        self.object_hook = object_hook
        self.encoder = encoder

        self._load()

    def _save(self):
        atomic_name = f"{uuid.uuid4()}.tmp"

        with open(atomic_name, "w", encoding="utf-8") as fp:
            json.dump(
                self._data.copy(), fp, ensure_ascii=True, cls=self.encoder, indent=2
            )

        os.replace(atomic_name, self.file)

    def _load(self):
        try:
            with open(self.file, "r", encoding="utf-8") as fp:
                self._data = json.load(fp, object_hook=self.object_hook)
        except FileNotFoundError:
            self._data = {}

    async def save(self):
        """Save the data in memory to disk."""
        async with self.lock:
            await self.loop.run_in_executor(None, self._save)

    async def load(self):
        """Load data from the JSON file on disk."""
        async with self.lock:
            await self.loop.run_in_executor(None, self._load)

    async def put(self, key, value):
        self._data[str(key)] = value
        await self.save()

    async def delete(self, key):
        del self._data[str(key)]
        await self.save()

    def get(self, key, *args):
        return self._data.get(str(key), *args)

    def all(self):
        return self._data

    def __contains__(self, key):
        return str(key) in self._data

    def __getitem__(self, key):
        return self._data[str(key)]

    def __len__(self):
        return len(self._data)
