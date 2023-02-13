from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import get_db, Base, SQLALCHEMY_DATABASE_URL
from app.main import app
import pytest
from app.utils.oauth2 import create_access_token
from app.entries.entries_model import Entry


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


@pytest.fixture
def test_user(client):
    user_create = {
        "firstname": "firstname",
        "lastname": "lastname",
        "email": "test@example.com",
        "password": "Password123",
        "cpassword": "Password123",
    }
    res = client.post("/account/signup", json=user_create)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_create["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_create = {
        "firstname": "firstname",
        "lastname": "lastname",
        "email": "test1@example.com",
        "password": "Password123",
        "cpassword": "Password123",
    }
    res = client.post("/account/signup", json=user_create)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_create["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_user(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_entry(test_user, database, test_user2):
    entry_data = [
        {
            "title": "Diary Log entry",
            "content": "Lets make some code",
            "owner_id": test_user["id"],
        },
        {
            "title": "Diary Postal entry",
            "content": "Lets make some code",
            "owner_id": test_user["id"],
        },
        {
            "title": "Diary catalogue entry",
            "content": "Lets make some code",
            "owner_id": test_user2["id"],
        },
    ]

    def create_entry_model(entry):
        return Entry(**entry)

    entry_map = map(create_entry_model, entry_data)
    entries = list(entry_map)
    database.add_all(entries)
    database.commit()
    entries = database.query(Entry).all()
    return entries
