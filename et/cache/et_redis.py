import contextlib
from datetime import datetime, timezone

import redis
from redis import Redis


class EtRedis:
    class Key:
        Page = "page"
        Token = "token"
        TokenUser = "user"
        DocTabUser = "user"
        DocTabAll = "all"
        DocTabTask = "task"

    def __init__(self, setting: dict):
        # self.pool = redis.ConnectionPool(
        #     host='automation-01.chengdudev.edetekapps.cn',
        #     port=9999,
        #     db=3,
        #     max_connections=10
        # )
        self.pool = redis.ConnectionPool(
            host=setting.get("REDIS_HOST"),
            port=setting.get("REDIS_PORT"),
            db=setting.get("REDIS_DB"),
            max_connections=setting.get("REDIS_MAX_CONNECTIONS")
        )

    @contextlib.contextmanager
    def r(self):
        _r = redis.Redis(connection_pool=self.pool)
        yield _r

    def init_cache(self, name: str):
        with self.r() as r:
            _r: Redis = r
            _r.hset(name, mapping={"pageTotal": 0})

    def increment_page_total(self, type_, user_id: str, number=1):
        with self.r() as r:
            _r: Redis = r
            _count = self.get_page_total(type_, user_id)
            if number > 0:
                r.hincrby(f'{self.Key.Page}:{type_}:{user_id}', "pageTotal", number)
            elif _count and _count > 0:
                r.hincrby(f'{self.Key.Page}:{type_}:{user_id}', "pageTotal", number)

    def set_page_total(self, type_, user_id, count: int):
        with self.r() as r:
            _r: Redis = r
            r.hincrby(f'{self.Key.Page}:{type_}:{user_id}', "pageTotal", count)

    def get_page_total(self, type_, user_id: str):
        with self.r() as r:
            _r: Redis = r
            result = _r.hget(f'{self.Key.Page}:{type_}:{user_id}', "pageTotal")
            return None if not result else int(result)
            # return int(_r.hget(name, "pageTotal"))

    def add_token(self, user_id, token, ex):
        with self.r() as r:
            _r: Redis = r
            _r.set(f"{self.Key.TokenUser}:{user_id}:token", token, ex=ex)

    def get_token(self, user_id):
        with self.r() as r:
            _r: Redis = r
            _token = _r.get(f"{self.Key.TokenUser}:{user_id}:token")
            _token = _token.decode() if _token else None
            return _token

    def set_last_active(self, user_id, ex):
        with self.r() as r:
            _r: Redis = r
            _r.set(f"{self.Key.TokenUser}:{user_id}:last_active", datetime.now(tz=timezone.utc).timestamp(), ex)

    def get_last_active(self, user_id):
        with self.r() as r:
            _r: Redis = r
            _active = _r.get(f"{self.Key.TokenUser}:{user_id}:last_active")
            _active = int(float(_r.get(f"{self.Key.TokenUser}:{user_id}:last_active").decode())) if _active else 0
            return _active

