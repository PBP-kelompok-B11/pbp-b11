from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from rafi_player.models import Player
from ibeth_clubs.models import Club
from search.models import SearchQuery

class SearchViewsTestCase(TestCase):
    def setUp(self):
        # Buat client untuk simulasi request
        self.client = Client()

        # Buat user dummy
        self.user = User.objects.create_user(username='tester', password='testpass123')

        # Buat data pemain & klub dummy
        self.player = Player.objects.create(
            nama="Lionel Messi",
            negara="Argentina",
            posisi="Forward",
            usia=36
        )

        self.club = Club.objects.create(
            nama="Barcelona",
            negara="Spanyol",
            stadion="Camp Nou"
        )

    def test_search_form_view(self):
        """Cek halaman form search bisa diakses"""
        response = self.client.get(reverse('search:search_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/form.html')

    def test_search_players_normal(self):
        """Cek pencarian pemain non-AJAX"""
        response = self.client.get(reverse('search:search_players'), {'q': 'Messi'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/results.html')
        self.assertContains(response, "Messi")

        self.assertTrue(SearchQuery.objects.filter(kata_kunci='Messi', jenis='pemain').exists())

    def test_search_players_ajax(self):
        """Cek pencarian pemain dengan AJAX (JSON response)"""
        response = self.client.get(
            reverse('search:search_players'),
            {'q': 'Messi'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(data['results'][0]['nama'], 'Lionel Messi')

    def test_search_clubs_normal(self):
        """Cek pencarian klub non-AJAX"""
        response = self.client.get(reverse('search:search_clubs'), {'q': 'Barcelona'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/results.html')
        self.assertContains(response, "Barcelona")

        # Pastikan query tersimpan
        self.assertTrue(SearchQuery.objects.filter(kata_kunci='Barcelona', jenis='klub').exists())

    def test_search_clubs_ajax(self):
        """Cek pencarian klub dengan AJAX (JSON response)"""
        response = self.client.get(
            reverse('search:search_clubs'),
            {'q': 'Barcelona'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(data['results'][0]['nama'], 'Barcelona')

    def test_search_history_requires_login(self):
        """Pastikan history cuma bisa diakses kalau login"""
        # Belum login → harus redirect ke login page
        response = self.client.get(reverse('search:search_history'))
        self.assertEqual(response.status_code, 302)  # redirect ke login

        # Setelah login → bisa akses
        self.client.login(username='tester', password='testpass123')
        response = self.client.get(reverse('search:search_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/history.html')