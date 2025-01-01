from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
import os
import pytest


URL = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}_test'
if URL is None:
    raise ValueError("No DATABASE_URL found in environment variables")

engine = create_engine(URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


client = TestClient(app)


# Drop all tables and recreate them before tests
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the get_db dependency to use the TestSessionLocal
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# Create a test user
@pytest.fixture
def test_user(client):
    user_data = {
        "email": "test1.create.user@gmail.com",
        "password": "testPassword1",
    }
    response = client.post("/users/", json=user_data)
    new_user = response.json()
    new_user["password"] = user_data["password"]
    assert response.status_code == 201
    return new_user


@pytest.fixture
def new_test_user(client):
    user_data = {
        "email": "test2.create.user@gmail.com",
        "password": "testPassword2",
    }
    response = client.post("/users/", json=user_data)
    new_user = response.json()
    new_user["password"] = user_data["password"]
    assert response.status_code == 201
    return new_user


# Create a test token for test_user
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


# Create a test token for new_test_user
@pytest.fixture
def new_token(new_test_user):
    return create_access_token({"user_id": new_test_user["id"]})


# Add the token to the client headers
@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


# Add the token to the client headers
@pytest.fixture
def new_authorized_client(client, new_token):
    client.headers = {**client.headers, "Authorization": f"Bearer {new_token}"}
    return client


# Add posts to the test database
@pytest.fixture
def test_posts(test_user, session):
    posts = [
        {
            "title": "Test Post Title 1",
            "content": "Test Content 1",
            "owner_id": test_user["id"],
        },
        {
            "title": "Test Post Title 2",
            "content": "Test Content 2",
            "owner_id": test_user["id"],
        },
        {
            "title": "Test Post Title 3",
            "content": "Test Content 3",
            "owner_id": test_user["id"],
        },
    ]

    post_map = map(lambda post: models.Post(**post), posts)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()

    return session.query(models.Post).all()
