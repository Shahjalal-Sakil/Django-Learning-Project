from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import Board, Topic, Post
from ..views import PostUpdateView


class PostUpdateTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Tell me about django')
        self.username= 'john'
        self.password = '12ab34cd'
        user = User.objects.create_user(username=self.username, email='john@example.com',password=self.password)
        self.topic = Topic.objects.create(subject='Hello, world', board=self.board, starter=user)
        self.post = Post.objects.create(message='Lorem ipsum dolor sit amet', topic=self.topic, created_by=user)
        self.url = reverse('edit_post', kwargs={
            'pk': self.board.pk,
            'topic_pk': self.topic.pk,
            'post_pk': self.post.pk
        })


class LoginRequiredPostUpdateTests(PostUpdateTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class UnauthorizedPostUpdateTests(PostUpdateTestCase):
    def setUp(self):
        super().setUp()
        username = 'jane'
        password = 'ab1234cd'
        user = User.objects.create_user(username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,404)


class PostUpdateViewTests(PostUpdateTestCase):
    str = 'some'


class SuccessfulPostUpdateViewTests(PostUpdateTestCase):
    str = 'soe'


class InvalidPostUpdateViewTests(PostUpdateTestCase):
    str ='some'
