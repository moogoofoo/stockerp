import pytest
import os
import sys
# ensure project src directory is on the path
topdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if topdir not in sys.path:
    sys.path.insert(0, topdir)

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import core.database as database

@pytest.fixture(autouse=True)
def in_memory_db(monkeypatch):
    # Use in-memory SQLite for tests
    test_engine = create_engine('sqlite:///:memory:')
    # Monkeypatch engine and SessionLocal
    from sqlalchemy.orm import sessionmaker, scoped_session
    monkeypatch.setattr(database, 'engine', test_engine)
    monkeypatch.setattr(database, 'SessionLocal', scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    ))
    return test_engine


def test_get_engine_returns_engine(in_memory_db):
    assert database.get_engine() is in_memory_db


def test_db_session_commit_and_rollback(in_memory_db):
    # Define a simple table
    metadata = MetaData()
    test_table = Table('test_table', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('name', String(10), nullable=False))
    metadata.create_all(in_memory_db)

    # Test commit
    with database.db_session() as session:
        session.execute(test_table.insert().values(name='foo'))
    # Verify insertion
    with database.db_session() as session:
        result = session.execute(test_table.select()).mappings().all()
        assert len(result) == 1
        assert result[0]['name'] == 'foo'

    # Test rollback on exception
    class CustomError(Exception):
        pass
    with pytest.raises(CustomError):
        with database.db_session() as session:
            session.execute(test_table.insert().values(name='bar'))
            raise CustomError
    # After rollback, only initial row remains
    with database.db_session() as session:
        result = session.execute(test_table.select()).mappings().all()
        assert len(result) == 1
        assert result[0]['name'] == 'foo'
