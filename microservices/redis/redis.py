import json

import redis
from redis.commands.json.path import Path

from consts.redis import FILES_LIST
from services.logger import Logger
from services.redis.redis_settings import RedisSettings


class Redis:
    def __init__(self, settings:RedisSettings, logger):
        self.settings = settings
        self.logger = logger

    def connect(self):
        self.conn = redis.Redis(host=self.settings.host, port=self.settings.port, decode_responses=True)

    def clean_up(self):
        if self.conn is not None:
            self.conn.close()

    def update(self, key, value):
        try:
            self.connect()
            r_value = self.conn.json().get(key)
            r_value[FILES_LIST].append(value)
            self.conn.json().set(key, Path.root_path() ,r_value)
        except Exception as e:
            self.logger.error(e)
        finally:
            self.clean_up()


