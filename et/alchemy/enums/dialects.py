import enum


class Dialects(enum.Enum):
    Postgresql = "postgresql+psycopg2"
    MysqlClient = "mysql+mysqldb"
    Pymysql = "mysql+pymysql"
    Sqlite = "sqlite"
