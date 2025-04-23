import contextlib

from alchemy.enums.dialects import Dialects


def database_url(support_database: Dialects, settings: dict):
    return (
        f"{support_database.value}://{settings['USER']}:"
        f"{settings['PASSWORD']}@"
        f"{settings['HOST']}:"
        f"{settings['PORT']}/"
        f"{settings['NAME']}")
