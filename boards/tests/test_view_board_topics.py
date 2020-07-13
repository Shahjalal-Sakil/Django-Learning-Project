from django.test import TestCase
from django.urls import resolve,reverse
from ..models import Board
from ..views import TopicListView


class BoardTopicTest(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django Discuss Board')

    def test_Board_Topic_Success_Status_Code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_Board_Topic_Not_Found_Status_Code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topic_url_resolve_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func.view_class, TopicListView)

    def test_board_topic_view_contain_navigation_links(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic',kwargs={'pk': 1})
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))
