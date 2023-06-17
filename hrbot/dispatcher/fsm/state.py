from .storage import BaseStorage, StorageAllData, StorageKey, StorageValue, StorageUserData
from contextlib import asynccontextmanager


class FSMDataManager:
    def __init__(self, storage: BaseStorage, user_id: str):
        self._storage: BaseStorage = storage
        self._user_id: StorageKey = user_id
        self._data: list[tuple[StorageKey, StorageValue]] = list()
        self._current_data: StorageUserData | None = dict()

    def __getitem__(self, item: StorageKey) -> StorageValue:
        if self._current_data:
            return self._current_data[item]
        raise KeyError(item)

    def __setitem__(self, key: StorageKey, value: StorageValue):
        self._data.append((key, value))

    async def save(self) :
        for data in self._data:
            await self._storage.set_data(self._user_id, data[0], data[1])


class FSMState:
    def __init__(self, storage: BaseStorage):
        self._storage: BaseStorage = storage

    async def set_state(self, user_id: str, state_name: str, **kwargs) -> None:
        """Sets the user state"""
        await self._storage.set_data(user_id, 'state_name', state_name, **kwargs)

    async def get_state(self, user_id: str) -> str | None:
        """Returns the current state of the user.
        If no user state is specified, returns None"""
        data: dict | None = await self._storage.get_data(user_id)
        if data:
            return data.get('state_name', None)
        return None

    async def finish(self, user_id: str) -> None:
        """Deletes all user data from the repository, including state"""
        await self._storage.clear(user_id)

    @asynccontextmanager
    async def data(self, user_id: str):
        data_obj = FSMDataManager(self._storage, user_id)
        data_obj._current_data = await data_obj._storage.get_data(user_id)
        try:
            yield data_obj
        finally:
            await data_obj.save()
