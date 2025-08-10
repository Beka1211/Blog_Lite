from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post, SubPost

class BlogLiteTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        data = {"title": "Test Post", "body": "Some content"}
        response = self.client.post("/api/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_create_post_with_subposts(self):
        data = {
            "title": "Main Post",
            "body": "Main body",
            "subposts": [
                {"title": "Sub 1", "body": "Body 1"},
                {"title": "Sub 2", "body": "Body 2"},
            ]
        }
        response = self.client.post("/api/posts/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.first()
        self.assertEqual(post.subposts.count(), 2)

    def test_update_post_with_subposts(self):
        post = Post.objects.create(title="Old", body="Old body", author=self.user)
        sub = SubPost.objects.create(post=post, title="Old sub", body="Old sub body")
        data = {
            "title": "Updated",
            "body": "Updated body",
            "subposts": [
                {"id": sub.id, "title": "Updated sub", "body": "Updated body"},
                {"title": "New sub", "body": "New body"}
            ]
        }
        response = self.client.put(f"/api/posts/{post.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, "Updated")
        self.assertEqual(post.subposts.count(), 2)

    def test_like_toggle_post(self):
        post = Post.objects.create(title="Like post", body="Body", author=self.user)
        url = f"/api/posts/{post.id}/like/"

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.likes.count(), 1)

        response = self.client.post(url)
        post.refresh_from_db()
        self.assertEqual(post.likes.count(), 0)

    def test_view_increment_post(self):
        post = Post.objects.create(title="View post", body="Body", author=self.user)
        url = f"/api/posts/{post.id}/view/"
        self.client.get(url)
        post.refresh_from_db()
        self.assertEqual(post.views_count, 1)
        self.client.get(url)
        post.refresh_from_db()
        self.assertEqual(post.views_count, 2)

    def test_like_toggle_subpost(self):
        post = Post.objects.create(title="Main", body="Body", author=self.user)
        subpost = SubPost.objects.create(post=post, title="Sub", body="Body")
        url = f"/api/subposts/{subpost.id}/like/"

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        subpost.refresh_from_db()
        self.assertEqual(subpost.likes.count(), 1)

        response = self.client.post(url)
        subpost.refresh_from_db()
        self.assertEqual(subpost.likes.count(), 0)

    def test_view_increment_subpost(self):
        post = Post.objects.create(title="Main", body="Body", author=self.user)
        subpost = SubPost.objects.create(post=post, title="Sub", body="Body")
        url = f"/api/subposts/{subpost.id}/view/"
        self.client.get(url)
        subpost.refresh_from_db()
        self.assertEqual(subpost.views_count, 1)
        self.client.get(url)
        subpost.refresh_from_db()
        self.assertEqual(subpost.views_count, 2)
