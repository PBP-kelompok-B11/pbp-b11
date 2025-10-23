from django.test import TestCase
from django.urls import reverse
from .models import Club, ClubRanking

class ClubViewsTests(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            nama="FC Test",
            negara="Testland",
            stadion="Test Arena",
            tahun_berdiri=1900
        )
        self.ranking = ClubRanking.objects.create(
            club=self.club,
            musim="2023/2024",
            peringkat=1
        )

    def test_club_list_view(self):
        resp = self.client.get(reverse('club_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "FC Test")

    def test_club_detail_view(self):
        resp = self.client.get(reverse('club_detail', args=[self.club.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Test Arena")
        self.assertContains(resp, "2023/2024")

    def test_create_club(self):
        resp = self.client.post(reverse('club_create'), {
            'nama': 'New Club',
            'negara': 'Nowhere',
            'stadion': 'New Stadium',
            'tahun_berdiri': 2000
        })
        # redirect to detail page after creation
        self.assertEqual(resp.status_code, 302)
        new = Club.objects.get(nama='New Club')
        self.assertEqual(new.negara, 'Nowhere')

    def test_update_club(self):
        resp = self.client.post(reverse('club_update', args=[self.club.pk]), {
            'nama': 'FC Test Updated',
            'negara': self.club.negara,
            'stadion': self.club.stadion,
            'tahun_berdiri': self.club.tahun_berdiri
        })
        self.assertEqual(resp.status_code, 302)
        self.club.refresh_from_db()
        self.assertEqual(self.club.nama, 'FC Test Updated')

    def test_delete_club(self):
        resp = self.client.post(reverse('club_delete', args=[self.club.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Club.objects.filter(pk=self.club.pk).exists())

    def test_create_ranking(self):
        resp = self.client.post(reverse('club_ranking_create', args=[self.club.pk]), {
            'musim': '2024/2025',
            'peringkat': 2
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(ClubRanking.objects.filter(musim='2024/2025', club=self.club).exists())

    def test_delete_ranking(self):
        resp = self.client.post(reverse('club_ranking_delete', args=[self.ranking.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(ClubRanking.objects.filter(pk=self.ranking.pk).exists())
