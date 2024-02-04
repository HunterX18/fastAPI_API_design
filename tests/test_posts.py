import pytest
from app.schemas.post import BasePostResponseSchema, PostResponseSchema

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts')

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts")
    assert res.status_code == 200

def test_unauthorized_user_get_one_post(client, test_posts): 
    res = client.get(f"/posts/{test_posts[0].id}")
    post = PostResponseSchema(**res.json())
    assert post.Post.id == test_posts[0].id
    assert res.status_code == 200
    

def test_get_post_not_exist(client, test_posts):
    res = client.get(f"/posts/123124")
    assert res.status_code == 404

@pytest.mark.parametrize("title, content, published", [
    ("new title", "new content", True),
    ("another", "content", False),
    ("hello", "world", False)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = BasePostResponseSchema(**res.json())
    assert res.status_code == 201
    assert created_post.title == title

    assert created_post.content == content 
    assert created_post.published == published 
    assert created_post.owner_id == test_user['id']

def test_unauthorized_create_post(client, test_user):
    res = client.post("/posts/", json={"title": "title", "content": "content" })

    assert res.status_code == 401

def test_unauthorized_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_authorized_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204 

def test_delete_post_not_exists(authorized_client, test_user):
    res = authorized_client.delete("/posts/12342134")

    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user2, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[4].id}")

    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json = data)
    updated_post = BasePostResponseSchema(**res.json())
    assert res.status_code == 202
    assert updated_post.title == data["title"]

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "id": test_posts[4].id
    }
    res = authorized_client.put(f"/posts/{test_posts[4].id}", json = data)
    assert res.status_code == 403 



def test_unauthorized_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401
    

def test_update_post_not_exists(authorized_client, test_user):
    data = {
        "title": "updated title",
        "id": 123124 
    }
    res = authorized_client.put("/posts/123124", json = data)

    assert res.status_code == 404

    
