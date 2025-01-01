from app import schemas


# check if the post response is the same as the test post
def validate_post_response(json_response, test_posts):
    response_posts = sorted(json_response, key=lambda x: x["Post"]["id"])
    test_posts_sorted = sorted(test_posts, key=lambda x: x.id)

    for i, post in enumerate(response_posts):
        post_data = post["Post"]
        post_response = schemas.PostResponse(**post_data)

        assert post_response.id == test_posts_sorted[i].id
        assert post_response.title == test_posts_sorted[i].title
        assert post_response.content == test_posts_sorted[i].content
        assert post_response.owner_id == test_posts_sorted[i].owner_id
        assert post_response.created_at == test_posts_sorted[i].created_at


# Test to get all posts with an authorized client
def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)
    validate_post_response(response.json(), test_posts)


# Test to create a new post with an authorized client
def test_create_post(authorized_client, test_user):
    post_data = {
        "title": "New Post Title",
        "content": "New Post Content",
        "published": True,
        "owner_id": test_user["id"],
    }
    response = authorized_client.post("/posts/", json=post_data)
    assert response.status_code == 201
    created_post = schemas.PostResponse(**response.json())
    assert created_post.title == post_data["title"]
    assert created_post.content == post_data["content"]
    assert created_post.published == post_data["published"]
    assert created_post.owner_id == post_data["owner_id"]


# Test to update an existing post with an authorized client
def test_update_post(authorized_client, test_posts):
    post_data = {
        "title": "Updated Post Title",
        "content": "Updated Post Content",
        "published": False,
    }
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=post_data)
    assert response.status_code == 200
    updated_post = schemas.PostResponse(**response.json())
    assert updated_post.title == post_data["title"]
    assert updated_post.content == post_data["content"]
    assert updated_post.published == post_data["published"]


# Test to get a single post with an authorized client
def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 200
    validate_post_response([response.json()], [test_posts[0]])


# Test to get all posts with an unauthorized client
def test_unauthorized_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401


# Test to get a single post with an unauthorized client
def test_unauthorized_get_one_post(client, test_posts):
    response = client.get("/posts/{test_posts[0].id}")
    assert response.status_code == 401


# Test to get a non-existent post with an authorized client
def test_get_not_exist_post(authorized_client, test_posts):
    response = authorized_client.get("/posts/100")
    assert response.status_code == 404


# Test to delete a post with an authorized client
def test_delete_post(authorized_client, test_posts):
    id = test_posts[0].id
    response = authorized_client.delete(f"/posts/{id}")
    assert response.status_code == 204
    response = authorized_client.get(f"/posts/{id}")
    assert response.status_code == 404


# Test to create a new post with an unauthorized client
def test_unauthorized_create_post(client, test_user):
    post_data = {
        "title": "New Post Title",
        "content": "New Post Content",
        "published": True,
        "owner_id": test_user["id"],
    }
    response = client.post("/posts/", json=post_data)
    assert response.status_code == 401


# Test to update an existing post with an unauthorized client
def test_unauthorized_update_post(client, test_posts):
    post_data = {
        "title": "Updated Post Title",
        "content": "Updated Post Content",
        "published": False,
    }
    response = client.put(f"/posts/{test_posts[0].id}", json=post_data)
    assert response.status_code == 401


# Test to delete a post with an unauthorized client
def test_unauthorized_delete_post(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


# Test to delete a post by another user
def test_delete_by_another_user(new_authorized_client, test_posts):
    id = test_posts[0].id
    response = new_authorized_client.delete(f"/posts/{id}")
    assert response.status_code == 403
    response = new_authorized_client.get(f"/posts/{id}")
    assert response.status_code == 200
    validate_post_response([response.json()], [test_posts[0]])


# Test to update a post by another user
def test_update_by_another_user(new_authorized_client, test_posts):
    post_data = {
        "title": "Updated Post Title",
        "content": "Updated Post Content",
        "published": False,
    }
    response = new_authorized_client.put(f"/posts/{test_posts[0].id}", json=post_data)
    assert response.status_code == 403
    response = new_authorized_client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 200
    validate_post_response([response.json()], [test_posts[0]])
