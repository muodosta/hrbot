import json
from typing import Optional

StorageKey = str
StorageValue = str | int
StorageUserData = dict[StorageKey, StorageValue]
StorageAllData = dict[str, StorageUserData]


class BaseStorage:
    async def set_data(self, user_id: StorageKey, key: StorageKey, value: StorageValue, **kwargs) -> None:
        """Loads user data into the storage"""
        pass

    async def get_data(self, user_id: StorageKey) -> StorageUserData | None:
        """Loads user data from storage"""
        pass

    async def get_all_data(self) -> StorageAllData | None:
        """Loads all data from storage"""
        pass

    async def clear(self, user_id: StorageKey) -> None:
        """Delete user data in storage"""
        pass


class Memory(BaseStorage):
    def __init__(self):
        self.data: StorageAllData = dict()

    async def set_data(self, user_id: StorageKey, key: StorageKey, value: StorageValue, **kwargs) -> None:
        if await self.get_data(user_id):
            self.data[user_id][key] = value
            return
        self.data[user_id] = {}
        self.data[user_id][key] = value

    async def get_data(self, user_id: StorageKey) -> StorageUserData | None:
        return self.data.get(user_id, None)

    async def get_all_data(self) -> StorageAllData | None:
        return self.data

    async def clear(self, user_id: StorageKey) -> None:
        del self.data[user_id]


class Redis(BaseStorage):
    def __init__(
            self,
            host: str = "localhost",
            port: int = 6379,
            db: Optional[int] = None,
            username: Optional[str] = None,
            password: Optional[str] = None,
            ssl: Optional[bool] = None,
            pool_size: int = 10,
            prefix: str = "fsm",
            ttl: Optional[int] = None,
            **kwargs,
    ):
        from redis import asyncio as aredis

        self._prefix = prefix
        self._ttl = ttl

        self._redis: aredis.Redis = aredis.Redis(
            host=host,
            port=port,
            db=db,
            username=username,
            password=password,
            ssl=ssl,
            max_connections=pool_size,
            decode_responses=True,
            **kwargs
        )

    def prefix(self, key: str):
        if key.startswith(self._prefix):
            return key.replace(self._prefix, '')
        return f'{self._prefix}{key}'

    async def set_data(self, user_id: StorageKey, key: StorageKey, value: StorageValue, **kwargs) -> None:
        if user_data := await self.get_data(user_id):
            user_data[key] = value
            await self._redis.set(self.prefix(user_id), json.dumps(user_data), ex=self._ttl, **kwargs)
            return
        await self._redis.set(self.prefix(user_id), json.dumps({key: value}), ex=self._ttl, **kwargs)

    async def get_data(self, user_id: StorageKey) -> StorageUserData | None:
        data = await self._redis.get(self.prefix(user_id))
        if data:
            return json.loads(data)
        return None

    async def get_all_data(self) -> StorageAllData | None:
        data: StorageAllData = {}
        async for key in self._redis.scan_iter(f'{self._prefix}*'):
            data[self.prefix(key)] = await self.get_data(self.prefix(key))
        return data

    async def clear(self, user_id: StorageKey) -> None:
        await self._redis.delete(self.prefix(user_id))


async def storage_test():
    user_id = '1'
    user_data_1 = ('name', 'Alexio')
    user_data_2 = ('age', 17)
    user_data = {**dict([user_data_1]), **dict([user_data_2])}

    print('Memory test: ', end='')
    memory = Memory()
    await memory.set_data(user_id, *user_data_1)
    await memory.set_data(user_id, *user_data_2)
    assert await memory.get_data(user_id) == user_data
    assert await memory.get_all_data() == {user_id: user_data}
    await memory.clear(user_id)
    assert await memory.get_all_data() == {}
    assert await memory.get_data(user_id) is None
    print('Done')

    print('Redis test: ', end='')
    redis = Redis(
        prefix='test_storage_fsm_',
        ttl=60
    )
    await redis.set_data(user_id, *user_data_1)
    await redis.set_data(user_id, *user_data_2)
    assert await redis.get_data(user_id) == user_data
    assert await redis.get_all_data() == {user_id: user_data}
    await redis.clear(user_id)
    assert await redis.get_all_data() == {}
    assert await redis.get_data(user_id) is None
    print('Done')

if __name__ == '__main__':
    import asyncio
    asyncio.run(storage_test())
