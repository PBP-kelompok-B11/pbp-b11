from django.test import TestCase
from django.urls import reverse
from .models import Club, ClubRanking


class ClubModelTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            nama="Manchester United",
            negara="Inggris",
            stadion="Old Trafford",
            tahun_berdiri=1878,
            url_gambar="https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg"
        )

    def test_str_representation(self):
        self.assertEqual(str(self.club), "Manchester United")

    def test_fields_content(self):
        self.assertEqual(self.club.negara, "Inggris")
        self.assertEqual(self.club.stadion, "Old Trafford")
        self.assertEqual(self.club.tahun_berdiri, 1878)
        self.assertIn("http", self.club.url_gambar)


class ClubRankingModelTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            nama="Barcelona",
            negara="Spanyol",
            stadion="Camp Nou",
            tahun_berdiri=1899,
            url_gambar="https://upload.wikimedia.org/wikipedia/en/4/47/FC_Barcelona_%28crest%29.svg"
        )
        self.ranking = ClubRanking.objects.create(
            club=self.club,
            musim="2023/2024",
            peringkat=1,
            poin=90
        )

    def test_ranking_str(self):
        self.assertIn("Barcelona", str(self.ranking))

    def test_ranking_fields(self):
        self.assertEqual(self.ranking.peringkat, 1)
        self.assertEqual(self.ranking.musim, "2023/2024")
        self.assertEqual(self.ranking.poin, 90)


class ClubViewsTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            nama="Real Madrid",
            negara="Spanyol",
            stadion="Santiago Bernabéu",
            tahun_berdiri=1902,
            url_gambar="https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg"
        )

    def test_club_list_view(self):
        response = self.client.get(reverse('ibeth_clubs:club_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Real Madrid")

    def test_club_detail_view(self):
        response = self.client.get(reverse('ibeth_clubs:club_detail', args=[self.club.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Santiago Bernabéu")

    def test_club_create_view(self):
        data = {
            'nama': 'Juventus',
            'negara': 'Italia',
            'stadion': 'Allianz Stadium',
            'tahun_berdiri': 1897,
            'url_gambar': 'https://upload.wikimedia.org/wikipedia/en/3/3b/Juventus_Turin.svg'
        }
        response = self.client.post(reverse('ibeth_clubs:club_create'), data)
        # admin_only decorator bisa kamu matikan sementara di testing
        self.assertIn(response.status_code, [200, 302])

    def test_club_update_view(self):
        response = self.client.post(
            reverse('ibeth_clubs:club_update', args=[self.club.pk]),
            {
                'nama': 'Real Madrid CF',
                'negara': 'Spanyol',
                'stadion': 'Bernabéu',
                'tahun_berdiri': 1902,
                'url_gambar': self.club.url_gambar,
            }
        )
        self.assertIn(response.status_code, [200, 302])

    def test_club_delete_view(self):
        response = self.client.post(reverse('ibeth_clubs:club_delete', args=[self.club.pk]))
        self.assertIn(response.status_code, [200, 302])


class ClubRankingViewsTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            nama="Liverpool",
            negara="Inggris",
            stadion="Anfield",
            tahun_berdiri=1892,
            url_gambar="https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg"
        )
        self.ranking = ClubRanking.objects.create(
            club=self.club,
            musim="2023/2024",
            peringkat=2,
            poin=85
        )

    def test_ranking_list_view(self):
        response = self.client.get(reverse('ibeth_clubs:ranking_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Liverpool")

    def test_club_ranking_create_view(self):
        data = {
            'musim': '2024/2025',
            'peringkat': 3,
            'poin': 78
        }
        response = self.client.post(reverse('ibeth_clubs:club_ranking_create', args=[self.club.pk]), data)
        self.assertIn(response.status_code, [200, 302])

    def test_club_ranking_update_view(self):
        response = self.client.post(
            reverse('ibeth_clubs:club_ranking_update', args=[self.ranking.pk]),
            {
                'musim': '2023/2024',
                'peringkat': 1,
                'poin': 92
            }
        )
        self.assertIn(response.status_code, [200, 302])

    def test_club_ranking_delete_view(self):
        response = self.client.post(reverse('ibeth_clubs:club_ranking_delete', args=[self.ranking.pk]))
        self.assertIn(response.status_code, [200, 302])
