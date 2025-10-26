from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Player, SeasonStats, CareerHistory, Achievement
import uuid

from rafi_player.models import Player

class PlayerModelTest(TestCase):
    """Test semua model di rafi_player"""

    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='12345')
        self.player = Player.objects.create(
            user=self.user,
            nama="Lionel Messi",
            negara="Argentina",
            posisi="FW",
            usia=36,
            tinggi=170,
            berat=72,
            thumbnail="https://example.com/messi.jpg"
        )
        self.stat = SeasonStats.objects.create(
            player=self.player, musim="2023/24", pertandingan=30, gol=25, assist=15, kartu=2
        )
        self.career = CareerHistory.objects.create(
            player=self.player, klub="Inter Miami", tahun_mulai=2023
        )
        self.ach = Achievement.objects.create(
            player=self.player, deskripsi="Ballon d'Or", tahun=2023
        )

    def test_str_methods(self):
        """Pastikan string representation benar"""
        self.assertEqual(str(self.player), "Lionel Messi")
        self.assertIn("Inter Miami", str(self.career))
        self.assertIn("2023/24", str(self.stat))
        self.assertIn("Ballon d'Or", str(self.ach))

    def test_related_fields(self):
        """Pastikan relasi foreign key bekerja"""
        self.assertEqual(self.player.riwayat_karier.count(), 1)
        self.assertEqual(self.player.statistik_musim.count(), 1)
        self.assertEqual(self.player.prestasi.count(), 1)


class PlayerViewsTest(TestCase):
    """Test semua view di rafi_player"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='viewer', password='pass123')
        self.client.login(username='viewer', password='pass123')
        self.player = Player.objects.create(
            user=self.user,
            nama="Kylian Mbappé",
            negara="France",
            posisi="FW",
            usia=25,
            tinggi=178,
            berat=73,
            thumbnail="https://example.com/mbappe.jpg"
        )

    def test_player_list_view(self):
        """Pastikan halaman player list bisa diakses"""
        url = reverse('rafi_player:player_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player_list.html')

    def test_json_list_view(self):
        """Cek endpoint show_json_player"""
        url = reverse('rafi_player:show_json_player')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(len(data), 0)
        self.assertEqual(data[0]['nama'], "Kylian Mbappé")

    def test_json_detail_view_valid(self):
        """Cek endpoint show_json_player_by_id"""
        url = reverse('rafi_player:show_json_player_by_id', args=[self.player.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['nama'], "Kylian Mbappé")

    def test_json_detail_view_invalid(self):
        """Cek jika ID tidak valid"""
        url = reverse('rafi_player:show_json_player_by_id', args=[uuid.uuid4()])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_add_player_success(self):
        """Tambah player baru via POST"""
        url = reverse('rafi_player:add_player_ajax')
        new_data = {
            "nama": "Erling Haaland",
            "negara": "Norway",
            "posisi": "FW",
            "usia": 23,
            "tinggi": 194,
            "berat": 88,
            "thumbnail": "https://example.com/haaland.jpg",
        }
        response = self.client.post(url, new_data)
        self.assertIn(response.status_code, [200, 201, 302])
        self.assertTrue(Player.objects.filter(nama="Erling Haaland").exists())

    def test_add_player_missing_field(self):
        """Coba tambah player tapi field kurang → 400"""
        url = reverse('rafi_player:add_player_ajax')
        incomplete_data = {
            "nama": "No Thumb",
            "negara": "Mars",
            "posisi": "DF",
            "usia": 20,
            "tinggi": 180,
            "berat": 70,
            # thumbnail hilang
        }
        response = self.client.post(url, incomplete_data)
        self.assertEqual(response.status_code, 400)

    def test_add_player_unauthenticated(self):
        """Coba tambah player tanpa login"""
        self.client.logout()
        url = reverse('rafi_player:add_player_ajax')
        response = self.client.post(url, {
            "nama": "Should Fail",
            "negara": "X",
            "usia": 10,
            "tinggi": 100,
            "berat": 50,
            "posisi": "MF",
            "thumbnail": "https://example.com/fail.jpg"
        })
        # redirect ke login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_delete_player_success(self):
        """Hapus player"""
        player = Player.objects.create(
            user=self.user,
            nama="Delete Me",
            negara="Nowhere",
            usia=22,
            tinggi=180,
            berat=70,
            posisi="GK",
            thumbnail="https://example.com/delete.jpg",
        )
        url = reverse('rafi_player:delete_player', args=[player.id])
        response = self.client.post(url)
        self.assertIn(response.status_code, [200, 302])
        self.assertFalse(Player.objects.filter(id=player.id).exists())

    def test_delete_player_not_found(self):
        """Hapus player yang tidak ada"""
        fake_id = uuid.uuid4()
        url = reverse('rafi_player:delete_player', args=[fake_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_player_list_requires_login(self):
        """Pastikan player list redirect kalau belum login"""
        self.client.logout()
        url = reverse('rafi_player:player_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)



class PlayerViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.player = Player.objects.create(
            user=self.user,
            nama='Test Player',
            negara='Testland',
            usia=25,
            tinggi=180,
            berat=75,
            posisi='FW',
            thumbnail='https://example.com/image.jpg'
        )

    def test_show_json_player(self):
        url = reverse('rafi_player:show_json_player')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Player', response.content.decode())

    def test_show_json_player_by_id_exists(self):
        url = reverse('rafi_player:show_json_player_by_id', args=[self.player.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Player', response.content.decode())

    def test_show_json_player_by_id_not_found(self):
        fake_id = uuid.uuid4()
        url = reverse('rafi_player:show_json_player_by_id', args=[fake_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_player_list_view(self):
        url = reverse('rafi_player:player_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player_list.html')
        self.assertContains(response, 'Test Player')

    def test_player_detail_view(self):
        url = reverse('rafi_player:player_detail', args=[self.player.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player_details.html')
        self.assertContains(response, self.player.nama)


    def test_add_player_ajax_requires_login(self):
        url = reverse('rafi_player:add_player_ajax')
        response = self.client.post(url, {
            'nama': 'Player2', 'negara': 'Negara', 'usia': 22,
            'tinggi': 175, 'berat': 70, 'posisi': 'MF', 'thumbnail': 'https://example.com/img.jpg'
        })
       
        self.assertEqual(response.status_code, 302)

    def test_add_player_ajax_logged_in(self):
        self.client.login(username='testuser', password='pass123')
        url = reverse('rafi_player:add_player_ajax')
        response = self.client.post(url, {
            'nama': 'Player2', 'negara': 'Negara', 'usia': 22,
            'tinggi': 175, 'berat': 70, 'posisi': 'MF', 'thumbnail': 'https://example.com/img.jpg'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'CREATED')
        self.assertTrue(Player.objects.filter(nama='Player2').exists())

    def test_edit_player_ajax_post(self):
        self.client.login(username='testuser', password='pass123')
        url = reverse('rafi_player:edit_player_ajax', args=[self.player.id])
        response = self.client.post(url, {
            'nama': 'Updated Name', 'negara': 'Newland', 'usia': 30,
            'tinggi': 185, 'berat': 80, 'posisi': 'GK', 'thumbnail': 'https://example.com/new.jpg'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.player.refresh_from_db()
        self.assertEqual(self.player.nama, 'Updated Name')

    def test_edit_player_ajax_get(self):
        url = reverse('rafi_player:edit_player_ajax', args=[self.player.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'error')

    
    def test_delete_player_post(self):
        self.client.login(username='testuser', password='pass123')
        url = reverse('rafi_player:delete_player', args=[self.player.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Player.objects.filter(id=self.player.id).exists())

class PlayerViewsEdgeCaseTest(TestCase):
        def setUp(self):
            self.client = Client()
            self.user = User.objects.create_user(username='edgeuser', password='pass123')
            self.player = Player.objects.create(
                user=self.user,
                nama='Edge Player',
                negara='Edgeland',
                usia=28,
                tinggi=180,
                berat=75,
                posisi='MF',
                thumbnail='https://example.com/edge.jpg'
            )

 
        def test_add_player_ajax_missing_fields(self):
            self.client.login(username='edgeuser', password='pass123')
            url = reverse('rafi_player:add_player_ajax')
            response = self.client.post(url, {
                'nama': 'Incomplete Player',
                # missing negara, usia, tinggi, berat, posisi, thumbnail
            })
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.content, b"Missing fields")

     
        def test_edit_player_ajax_not_found(self):
            self.client.login(username='edgeuser', password='pass123')
            fake_id = uuid.uuid4()
            url = reverse('rafi_player:edit_player_ajax', args=[fake_id])
            response = self.client.post(url, {
                'nama': 'DoesNotExist'
            })
            self.assertEqual(response.status_code, 404)

        
        def test_delete_player_not_found(self):
            self.client.login(username='edgeuser', password='pass123')
            fake_id = uuid.uuid4()
            url = reverse('rafi_player:delete_player', args=[fake_id])
            response = self.client.post(url)
            self.assertEqual(response.status_code, 404)

        
        def test_show_json_player_empty(self):
            Player.objects.all().delete()
            url = reverse('rafi_player:show_json_player')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data, [])

        
        def test_player_create_post_invalid(self):
            self.client.login(username='edgeuser', password='pass123')
            url = reverse('rafi_player:player_create')
            response = self.client.post(url, {
                'nama': '',  # invalid, empty field
                'negara': 'Invalidland'
            })
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'player_form.html')
            self.assertContains(response, 'This field is required', html=True)

class PlayerViewsCoverageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.player = Player.objects.create(
            user=self.user,
            nama='Test Player',
            negara='Testland',
            usia=25,
            tinggi=175,
            berat=70,
            posisi='MF',
            thumbnail='https://example.com/test.jpg'
        )

    def test_edit_player_ajax_get_method_error(self):
        self.client.login(username='testuser', password='pass123')
        url = reverse('rafi_player:edit_player_ajax', args=[self.player.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('Invalid method', data['message'])

    def test_delete_player_success_redirect(self):
        self.client.login(username='testuser', password='pass123')
        url = reverse('rafi_player:delete_player', args=[self.player.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('rafi_player:player_list'), response.url)
        self.assertFalse(Player.objects.filter(id=self.player.id).exists())


    def test_player_detail_view(self):
        url = reverse('rafi_player:player_detail', args=[self.player.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player_details.html')
        self.assertContains(response, self.player.nama)

    
    def test_player_list_view(self):
        url = reverse('rafi_player:player_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player_list.html')
        self.assertContains(response, self.player.nama)

    def test_player_create_get(self):
        self.client.login(username='testuser', password='pass123')
        url = reverse('rafi_player:player_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player_form.html')
        self.assertIsInstance(response.context['form'], PlayerForm)

    def test_show_json_player_by_id_success(self):
        url = reverse('rafi_player:show_json_player_by_id', args=[self.player.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['nama'], self.player.nama)
        self.assertEqual(data['user_id'], self.user.id)
        self.assertEqual(data['user_username'], self.user.username)

class PlayerViewsExtraCoverageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.player = Player.objects.create(
            user=self.user,
            nama='Test Player',
            negara='Testland',
            usia=25,
            tinggi=175,
            berat=70,
            posisi='MF',
            thumbnail='https://example.com/test.jpg'
        )

    def test_add_player_ajax_missing_fields(self):
        self.client.login(username='testuser', password='pass123')
        url = reverse('rafi_player:add_player_ajax')
        response = self.client.post(url, {
            'nama': 'Incomplete Player', 
    
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing fields', response.content)

    def test_add_player_ajax_not_logged_in(self):
        url = reverse('rafi_player:add_player_ajax')
        response = self.client.post(url, {
            'nama': 'Test',
            'negara': 'X',
            'usia': 20,
            'tinggi': 170,
            'berat': 65,
            'posisi': 'MF',
            'thumbnail': 'https://example.com/a.jpg'
        })
    
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_show_json_player_empty(self):
        Player.objects.all().delete()
        url = reverse('rafi_player:show_json_player')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, [])

    def test_player_create_post_invalid_form(self):
        self.client.login(username='testuser', password='pass123')
        url = reverse('rafi_player:player_create')
        response = self.client.post(url, {'nama': ''})  # invalid: nama kosong
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player_form.html')
        self.assertIsInstance(response.context['form'], PlayerForm)
        self.assertFalse(response.context['form'].is_valid())

    def test_edit_player_ajax_invalid_method(self):
        self.client.login(username=self.user.username, password='pass')
        player = Player.objects.create(user=self.user, nama="A", negara="B", usia=20, tinggi=180, berat=70, posisi="FW", thumbnail="")
        response = self.client.get(reverse('rafi_player:edit_player_ajax', args=[player.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'error')

    #tes