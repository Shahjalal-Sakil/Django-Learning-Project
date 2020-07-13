from django.test import TestCase
from django.urls import resolve,reverse
from ..models import Board
from ..views import HomeListView


class HomeTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django Discuss Board')
        url = reverse('home')
        self.response = self.client.get(url)

    def home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolve_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, HomeListView)

    def test_home_view_contain_link_to_board_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))
