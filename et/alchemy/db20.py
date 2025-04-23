import contextlib
from typing import Generator

from sqlalchemy import create_engine, QueuePool
from sqlalchemy.orm import sessionmaker, Session

from alchemy.enums.dialects import Dialects
from alchemy.helper import database_url


class Db:
    def __init__(self, dialect: Dialects, settings: dict):
        # 避免MYSQl 8 小时自动释放空连接
        self.engine = create_engine(database_url(dialect, settings), poolclass=QueuePool,
                                    pool_size=10,  # 连接池大小
                                    max_overflow=10,  # 连接池最大溢出大小
                                    pool_recycle=3600,  # 连接池回收时间（1 小时）
                                    pool_pre_ping=True,  # 启用连接预检,在每次连接前会先执行一个简单的查询来查询链接是否仍然有效
                                    pool_timeout=30,  # 获取连接的超时时间（秒
                                    echo=True # 日志
                                    )

    @contextlib.contextmanager
    def session(self, autoflush=True, autobegin=True):
        _session = None
        try:
            _session = sessionmaker(bind=self.engine, autoflush=autoflush, autobegin=autobegin)()
            yield _session
        finally:
            _session.close()
