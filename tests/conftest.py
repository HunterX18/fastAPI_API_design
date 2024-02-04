from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.db.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models.models import PostModel
from app.utils.oauth import create_access_token

engine = create_engine(settings.testing_db_url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password"}
    res = client.post("/users", json = user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "hello@gmail.com", "password": "password"}
    res = client.post("/users", json = user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user
    
@pytest.fixture
def token(test_user):
    return create_access_token({ "user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "title 1",
            "content": "content 1",
            "owner_id": test_user["id"]
        },
        {
            "title": "title 2",
            "content": "content 2",
            "owner_id": test_user["id"]
        },
        {
            "title": "title 3",
            "content": "content 3",
            "owner_id": test_user["id"]
        },
        {
            "title": "title 4",
            "content": "content 4",
            "owner_id": test_user["id"]
        },
        {
            "title": "title 5",
            "content": "content 5",
            "owner_id": test_user2["id"]
        },
    ]

    def create_post_model(post):
        return PostModel(**post)
    
    posts_map = map(create_post_model, posts_data)
    posts_list = list(posts_map)

    session.add_all(posts_list)
    session.commit()
    posts = session.query(PostModel).all()
    return posts
