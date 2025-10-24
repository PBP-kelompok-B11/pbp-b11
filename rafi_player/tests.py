from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Player
from .forms import PlayerForm
import uuid

class PlayerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass1234')
        self.player = Player.objects.create(
            nama='John Doe',
            negara='Wonderland',
            usia=20,
            tinggi=180,
            berat=70,
            posisi='Striker',
            thumbnail='https://placehold.co/300x400',
            user=self.user
        )

    def test_player_creation(self):
        self.assertEqual(self.player.nama, 'John Doe')
        self.assertEqual(self.player.user.username, 'tester')
        self.assertTrue(isinstance(self.player.id, uuid.UUID))

class PlayerFormTest(TestCase):
    def test_player_form_valid(self):
        form_data = {
            'nama': 'Jane Doe',
            'negara': 'Wonderland',
            'usia': 19,
            'tinggi': 165,
            'berat': 55,
            'posisi': 'Bek',
            'thumbnail': 'https://placehold.co/300x400',
        }
        form = PlayerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_player_form_invalid(self):
        form_data = {
            'nama': '',
            'negara': 'Wonderland',
            'usia': 19,
            'tinggi': 165,
            'berat': 55,
            'posisi': 'Bek',
            'thumbnail': 'https://placehold.co/300x400',
        }
        form = PlayerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nama', form.errors)

class PlayerViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='pass1234')
        self.client.login(username='tester', password='pass1234')

        self.player = Player.objects.create(
            nama='John Doe',
            negara='Wonderland',
            usia=20,
            tinggi=180,
            berat=70,
            posisi='Striker',
            thumbnail='https://placehold.co/300x400',
            user=self.user
        )

    def test_show_json_player(self):
        url = reverse('rafi_player:show_json_player')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]['nama'], 'John Doe')

    def test_show_json_player_by_id(self):
        url = reverse('rafi_player:show_json_player_by_id', args=[self.player.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['nama'], 'John Doe')
        self.assertEqual(data['user_username'], 'tester')

    def test_player_list_view(self):
        url = reverse('rafi_player:player_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_player_detail_view(self):
        url = reverse('rafi_player:player_detail', args=[self.player.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_add_player_ajax_view(self):
        url = reverse('rafi_player:add_player_ajax')
        data = {
            'nama': 'Alice',
            'negara': 'Wonderland',
            'usia': 18,
            'tinggi': 160,
            'berat': 50,
            'posisi': 'Gelandang',
            'thumbnail': 'https://placehold.co/300x400',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'CREATED')
        self.assertTrue(Player.objects.filter(nama='Alice').exists())

    def test_edit_player_ajax_view(self):
        url = reverse('rafi_player:edit_player_ajax', args=[self.player.id])
        data = {'nama': 'John Updated'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.player.refresh_from_db()
        self.assertEqual(self.player.nama, 'John Updated')

    def test_delete_player_view(self):
        url = reverse('rafi_player:delete_player', args=[self.player.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('rafi_player:player_list'))
        self.assertFalse(Player.objects.filter(id=self.player.id).exists())
