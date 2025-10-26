from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from comments.models import Comments
from vidia_event.models import Event
from ibeth_clubs.models import Club
from rafi_player.models import Player
import uuid
from datetime import date


class CommentsViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='12345')
        self.client.login(username='tester', password='12345')

        self.event = Event.objects.create(
            nama_event='Test Event',
            tipe='liga',
            lokasi='Jakarta',
            tanggal_mulai=date.today(),
            tanggal_selesai=date.today(),
            created_by=self.user
        )

        self.club = Club.objects.create(
            nama='Test Club',
            tahun_berdiri=2000,
        )

        self.player = Player.objects.create(
            user=self.user,
            id=uuid.uuid4(),
            nama='Test Player',
            usia=19,
            tinggi=175,
            berat=60,
            posisi='FW',
        )

    # ===============================
    # ADD COMMENT TESTS
    # ===============================
    def test_add_comment_to_event(self):
        url = reverse('comments:add_comment_to_event', args=[self.event.id])
        response = self.client.post(url, {'isi_komentar': 'Komentar event'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comments.objects.filter(isi_komentar='Komentar event').exists())

    def test_add_comment_to_club(self):
        url = reverse('comments:add_comment_to_club', args=[self.club.id])
        response = self.client.post(url, {'isi_komentar': 'Komentar club'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comments.objects.filter(isi_komentar='Komentar club').exists())

    def test_add_comment_to_player(self):
        url = reverse('comments:add_comment_to_player', args=[self.player.id])
        response = self.client.post(url, {'isi_komentar': 'Komentar player'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comments.objects.filter(isi_komentar='Komentar player').exists())

    # ===============================
    # EDIT COMMENT TEST
    # ===============================
    def test_edit_comment(self):
        comment = Comments.objects.create(
            user=self.user,
            isi_komentar='Old comment',
            content_type=ContentType.objects.get_for_model(self.club),
            object_id=self.club.id,
        )

        url = reverse('comments:edit_comment', args=[comment.id])
        response = self.client.post(url, {'isi_komentar': 'Edited comment'}, follow=True)
        self.assertEqual(response.status_code, 200)

        comment.refresh_from_db()
        self.assertEqual(comment.isi_komentar, 'Edited comment')

    # ===============================
    # DELETE COMMENT TEST
    # ===============================
    def test_delete_comment(self):
        comment = Comments.objects.create(
            user=self.user,
            isi_komentar='To be deleted',
            content_type=ContentType.objects.get_for_model(self.event),
            object_id=self.event.id,
        )

        url = reverse('comments:delete_comment', args=[comment.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comments.objects.filter(id=comment.id).exists())

    # ===============================
    # COMMENT LIST TEST
    # ===============================
    # def test_comment_list(self):
    #     Comments.objects.create(
    #         user=self.user,
    #         isi_komentar='List test comment',
    #         content_type=ContentType.objects.get_for_model(self.club),
    #         object_id=self.club.id,
    #     )

    #     url = reverse('comments:comment_list', args=['ibeth_clubs', 'club', self.club.id])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'List test comment', html=False)


