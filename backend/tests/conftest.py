"""This file sets up a test db, db session, and db client for our database tests."""

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
import time
import sqlalchemy
from app.core.cache import get_redis, CacheService
import redis


TEST_DATABASE_URL = "postgresql://test:test@localhost:5433/test_db"
TEST_REDIS_URL = "redis://localhost:6380"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
test_redis_client = redis.from_url(TEST_REDIS_URL, decode_responses=True)


@pytest.fixture(scope="session", autouse=True)
def start_db():
    os.system("docker-compose -f docker-compose.test.yml up -d")

    # wait for postgres to actually be ready
    for i in range(20):
        try:
            engine.connect()
            break
        except sqlalchemy.exc.OperationalError:
            time.sleep(1)
    else:
        raise RuntimeError("Postgres did not start in time")

    Base.metadata.create_all(bind=engine)
    yield
    os.system("docker-compose -f docker-compose.test.yml down -v")


@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def cache():
    cache_service = CacheService(test_redis_client)
    yield cache_service
    test_redis_client.flushdb()


@pytest.fixture(scope="function")
def client(db, cache):
    def override_get_db():
        yield db

    def override_get_redis():
        return cache

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    yield TestClient(app)
    app.dependency_overrides.clear()
