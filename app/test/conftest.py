from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import get_db, Base, SQLALCHEMY_DATABASE_URL
from app.main import app
import pytest


TEST_DATABASE = f"{SQLALCHEMY_DATABASE_URL}_test"

engine = create_engine(TEST_DATABASE, future=True)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(database):
    def override_get_db():
        try:
            yield database
        finally:
            database.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
