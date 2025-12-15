import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import SearchQuery
from rafi_player.models import Player
from ibeth_clubs.models import Club
from vidia_event.models import Event
from django.utils import timezone

class SearchViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass')
        # buat sample data
        self.player = Player.objects.create(nama='Lionel Messi', posisi='Forward', negara='Argentina')
        self.club = Club.objects.create(nama='FC Barcelona', negara='Spain', stadion='Camp Nou')
        self.event = Event.objects.create(nama_event='Champions League Final')

    # --------------------
    # Serialization
    # --------------------
    def test_show_json(self):
        SearchQuery.objects.create(kata_kunci='test', jenis='pemain', tanggal=timezone.now())
        response = self.client.get(reverse('search:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_xml_by_id(self):
        sq = SearchQuery.objects.create(kata_kunci='test', jenis='pemain', tanggal=timezone.now())
        response = self.client.get(reverse('search:show_xml_by_id', args=[sq.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    # --------------------
    # Redirect form
    # --------------------
    def test_search_redirect_players(self):
        response = self.client.get(reverse('search:search_redirect') + '?q=test&type=players')
        self.assertEqual(response.status_code, 302)
        self.assertIn('search_players', response.url)

    def test_search_redirect_clubs(self):
        response = self.client.get(reverse('search:search_redirect') + '?q=test&type=clubs')
        self.assertEqual(response.status_code, 302)
        self.assertIn('search_clubs', response.url)

    def test_search_redirect_events(self):
        response = self.client.get(reverse('search:search_redirect') + '?q=test&type=events')
        self.assertEqual(response.status_code, 302)
        self.assertIn('search_events', response.url)

    def test_search_redirect_empty_query(self):
        response = self.client.get(reverse('search:search_redirect') + '?q=')
        self.assertEqual(response.status_code, 302)
        self.assertIn('search_form', response.url)

    # --------------------
    # Search Players
    # --------------------
    def test_search_players_regular(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('search:search_players') + '?q=Lionel')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lionel Messi')

    def test_search_players_ajax(self):
        response = self.client.get(
            reverse('search:search_players') + '?q=Lionel',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['results'][0]['nama'], 'Lionel Messi')

    # --------------------
    # Search Clubs
    # --------------------
    def test_search_clubs_regular(self):
        response = self.client.get(reverse('search:search_clubs') + '?q=Barcelona')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'FC Barcelona')

    def test_search_clubs_ajax(self):
        response = self.client.get(
            reverse('search:search_clubs') + '?q=Barcelona',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['results'][0]['nama'], 'FC Barcelona')

    # --------------------
    # Search Events
    # --------------------
    def test_search_events_regular(self):
        response = self.client.get(reverse('search:search_events') + '?q=Champions')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Champions League Final')

    def test_search_events_ajax(self):
        response = self.client.get(
            reverse('search:search_events') + '?q=Champions',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['results'][0]['nama_event'], 'Champions League Final')

    # --------------------
    # Search Form
    # --------------------
    def test_search_form(self):
        response = self.client.get(reverse('search:search_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/form.html')
