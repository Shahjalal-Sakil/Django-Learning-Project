from django.test import TestCase
from django.urls import resolve,reverse
from ..models import Board,Topic,Post
from ..views import new_topic
from ..forms import NewTopicForm
from django.contrib.auth.models import User


class NewTopicTest(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django Discuss Board')
        User.objects.create_user(username='sakil', email='example@y.com',password='ab12cd34')
        self.client.login(username='sakil',password='ab12cd34')

    def test_new_topic_success_status_code(self):
        url = reverse('new_topic',kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolve_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_contain_link_back_to_board_topics(self):
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        board_topic_url = reverse('board_topics', kwargs={'pk':1})
        self.assertContains(response, 'href="{0}"'.format(board_topic_url))

    def test_csrf(self):
        url = reverse('new_topic',kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_post_valid_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test Subject',
            'message': 'Test Message'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_post_invalid_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code,200)
        self.assertTrue(form.errors)

    def test_new_topic_post_invalid_data_empty_field(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data={
            'subject':'',
            'message':''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contain_form(self):
        url = reverse('new_topic',kwargs={'pk':1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form,NewTopicForm)


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        self.url = reverse('new_topic',kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response,'{login_url}?next={url}'.format(login_url=login_url,url=self.url))
