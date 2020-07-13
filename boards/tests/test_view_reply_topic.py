from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from ..models import Board, Topic, Post
from ..views import reply_topic



class ReplyTopicTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.username = 'john'
        self.password = '12ab34cd'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.topic = Topic.objects.create(subject='Hello, world', board=self.board, starter=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', topic=self.topic, created_by=user)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})


class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    def some(self):
        return


class ReplyTopicTests(ReplyTopicTestCase):
    def some(self):
        return


class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def test_redirection(self):
        url = reverse('topic_posts', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        topic_posts_url = '{url}?page=1#2'.format(url=url)
        self.assertRedirects(self.response, topic_posts_url)


class InvalidReplyTopicTests(ReplyTopicTestCase):
    def some(self):
        return








