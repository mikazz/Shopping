import logging

import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(conn_str) -> None:
    """Session factory"""
    global __factory

    if __factory:
        return

    if not conn_str or not conn_str.strip():
        raise Exception("You must specify connection string")

    logger.debug(f"Connecting to the database: {conn_str}")

    engine = create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


def close_session():
    return __factory().close()

