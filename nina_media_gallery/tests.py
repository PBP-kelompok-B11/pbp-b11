from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from authentication.models import UserProfile
from nina_media_gallery.models import Media

class GalleryViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.object.create_user(username='admin_test', password='password')
        UserProfile.objects.create(user=self.admin_user, role='admin')
        self.client.force_login(self.admin_user)
        
        self.media1 = Media.objects.create(
            deskripsi="Foto Pantai",
            category="foto",
            thumbnail="https://example.com/img1.jpg",
        )
        self.media2 = Media.objects.create(
            deskripsi="Video Air Terjun",
            category="video",
            thumbnail="https://example.com/video-thumb.jpg",
        )

    def test_gallery_list(self):
        response = self.client.get(reverse('nina_media_gallery:gallery_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery_list.html')
        self.assertContains(response, "Foto Pantai")
        self.assertContains(response, "Video Air Terjun")

    def test_gallery_details_increment_views(self):
        url = reverse('nina_media_gallery:gallery_details', args=[self.media1.id])
        self.client.get(url)
        self.media1.refresh_from_db()
        self.assertEqual(self.media1.viewers, 1)

    def test_gallery_upload_POST(self):
        response = self.client.post(
            reverse('nina_media_gallery:gallery_upload'),
            {'deskripsi': 'Test upload', 'category': 'foto'}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Media.objects.count(), 3)

    def test_gallery_upload_invalid(self):
        response = self.client.post(
            reverse('nina_media_gallery:gallery_upload'),
            {'deskripsi': '', 'category': 'foto'}
        )
        self.assertEqual(response.status_code, 400)

    def test_gallery_update(self):
        response = self.client.post(
            reverse('nina_media_gallery:gallery_update', args=[self.media1.id]),
            {'deskripsi': 'Updated', 'category': 'video', 'thumbnail': ''}
        )
        self.assertEqual(response.status_code, 200)
        updated_media = Media.objects.get(id=self.media1.id)
        self.assertEqual(updated_media.deskripsi, 'Updated')
        self.assertEqual(updated_media.category, 'video')

    def test_gallery_update_invalid_method(self):
        response = self.client.get(
            reverse('nina_media_gallery:gallery_update', args=[self.media1.id])
        )
        self.assertEqual(response.status_code, 200)  # JSON error response

    def test_gallery_delete(self):
        response = self.client.get(
            reverse('nina_media_gallery:gallery_delete', args=[self.media1.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Media.objects.filter(id=self.media1.id).exists())

    def test_increment_views(self):
        media = Media.objects.create(deskripsi="Test View", category="foto")
        media.increment_views()
        media.increment_views()
        self.assertEqual(media.viewers, 2)