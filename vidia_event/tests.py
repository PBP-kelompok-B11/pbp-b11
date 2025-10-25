from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Event
from datetime import date

class EventModelTest(TestCase):
    def test_create_event(self):
        event = Event.objects.create(
            nama_event="Turnamen Sepakbola",
            tipe=Event.TURNAMEN,
            lokasi="Jakarta",
            tanggal_mulai=date(2025, 11, 1),
            tanggal_selesai=date(2025, 11, 5)
        )
        self.assertEqual(str(event), "Turnamen Sepakbola")
        self.assertEqual(event.tipe, Event.TURNAMEN)

class EventViewsTest(TestCase):
    def setUp(self):
        # buat user admin dan user biasa
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', is_staff=True)
        self.normal_user = User.objects.create_user(username='user', password='userpass')
        self.client = Client()
        # buat sample event
        self.event = Event.objects.create(
            nama_event="Liga Nasional",
            tipe=Event.LIGA,
            lokasi="Bandung",
            tanggal_mulai=date(2025, 10, 1),
            tanggal_selesai=date(2025, 10, 10)
        )

    def test_event_list_view(self):
        response = self.client.get(reverse('vidia_event:event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Liga Nasional")

    def test_event_detail_view(self):
        response = self.client.get(reverse('vidia_event:event_detail', args=[self.event.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bandung")

    def test_event_create_view_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('vidia_event:event_create'), {
            'event': 'Turnamen U-20',
            'tipe': Event.TURNAMEN,
            'lokasi': 'Surabaya',
            'start_date': '2025-12-01',
            'end_date': '2025-12-05'
        })
        self.assertRedirects(response, reverse('vidia_event:event_list'))
        self.assertTrue(Event.objects.filter(nama_event='Turnamen U-20').exists())

    def test_event_create_view_non_admin(self):
        self.client.login(username='user', password='userpass')
        response = self.client.post(reverse('vidia_event:event_create'), {
            'event': 'Turnamen U-18',
            'tipe': Event.TURNAMEN,
            'lokasi': 'Medan',
            'start_date': '2025-11-01',
            'end_date': '2025-11-05'
        })
        self.assertEqual(response.status_code, 403)  # admin_only harusnya blokir

    def test_event_update_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('vidia_event:event_update', args=[self.event.pk]), {
            'event': 'Liga Nasional Updated',
            'tipe': Event.LIGA,
            'lokasi': 'Jakarta',
            'start_date': '2025-10-02',
            'end_date': '2025-10-12'
        })
        self.assertRedirects(response, reverse('vidia_event:event_detail', args=[self.event.pk]))
        self.event.refresh_from_db()
        self.assertEqual(self.event.nama_event, 'Liga Nasional Updated')
        self.assertEqual(self.event.lokasi, 'Jakarta')

    def test_event_delete_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('vidia_event:event_delete', args=[self.event.pk]))
        self.assertRedirects(response, reverse('vidia_event:event_list'))
        self.assertFalse(Event.objects.filter(pk=self.event.pk).exists())
