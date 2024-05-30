from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase

from django.urls import reverse

from users.models import User
from education_content.models import Chapter, Material, MaterialPhotos

from django.test import SimpleTestCase
from education_content.templatetags.my_tags import mediapath_filter, get_item, mediapath


class ChapterControllerTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(email='testuser', password='testpassword')

    def test_chapter_create_view(self):
        self.client.login(email='testuser', password='testpassword')
        response = self.client.post(reverse('education_content:chapter_create'),
                                    {'title': 'Test Chapter', 'description': 'Test Chapter'})
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect

        # Check that the Chapter object was created
        created_chapter = Chapter.objects.filter(title='Test Chapter', description='Test Chapter').first()
        self.assertIsNotNone(created_chapter)

    def test_chapter_delete_view(self):
        self.client.login(email='testuser', password='testpassword')
        created_chapter = Chapter.objects.create(title='Test Chapter', description='Test Chapter')
        created_chapter.save()
        self.client.post(
            reverse('education_content:chapter_delete', kwargs={'pk': created_chapter.pk}))

        # Check that the Chapter object was deleted
        created_chapter = Chapter.objects.filter(title='Test Chapter', description='Test Chapter').first()
        self.assertIsNone(created_chapter)

    def test_chapter_update_view(self):
        self.client.login(email='testuser', password='testpassword')
        created_chapter = Chapter.objects.create(title='Test Chapter', description='Test Chapter')
        created_chapter.save()
        self.client.post(
            reverse('education_content:chapter_edit', kwargs={'pk': created_chapter.pk}),
            {'title': 'Test Chapter new', 'description': 'Test Chapter new'})

        # Check that the Chapter object was deleted
        created_chapter = Chapter.objects.filter(title='Test Chapter new', description='Test Chapter new').first()
        self.assertIsNotNone(created_chapter)

    def test_chapter_list_view(self):
        self.client.login(email='testuser', password='testpassword')
        response = self.client.get(reverse('education_content:chapter_list'))
        self.assertEqual(response.status_code, 200)  # Check for a successful response

    def test_chapter_detail_view(self):
        self.client.login(email='testuser', password='testpassword')
        chapter = Chapter.objects.create(title='Test Chapter', owner=self.user)
        response = self.client.get(reverse('education_content:chapter_view', kwargs={'pk': chapter.pk}))
        self.assertEqual(response.status_code, 200)  # Check for a successful response


class MaterialControllerTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(email='testuser', password='testpassword')
        # Create a test chapter
        self.chapter = Chapter.objects.create(title='Test Chapter', owner=self.user, description='Test Chapter')

    def test_material_create_view(self):
        self.client.login(email='testuser', password='testpassword')
        response = self.client.post(
            reverse('education_content:material_create'),
            {'topic': 'Test Material', 'text': 'Test Material', 'chapter': self.chapter.pk})
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect

        # Check that the Material object was created
        created_material = Material.objects.filter(topic='Test Material', text='Test Material').first()
        self.assertIsNotNone(created_material)

        request = self.client.get(
            reverse('education_content:material_create'))

        # Check for the 'chapter_list' parameter in the response context
        self.assertIn('chapter_list', request.context)

    def test_material_create_for_special_chapter_view(self):
        self.client.login(email='testuser', password='testpassword')
        response = self.client.post(
            reverse('education_content:material_create_for_special_chapter', kwargs={'chapter_pk': self.chapter.pk}),
            {'topic': 'Test Material 2', 'text': 'Test Material 2', 'chapter': self.chapter.pk})
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect

        # Check that the Material object was created
        created_material = Material.objects.filter(topic='Test Material 2', text='Test Material 2').first()
        self.assertIsNotNone(created_material)

        request = self.client.get(
            reverse('education_content:material_create_for_special_chapter', kwargs={'chapter_pk': self.chapter.pk}))

        # Check for the 'chapter_pk' parameter in the response context
        self.assertIn('chapter_pk', request.context)

    def test_material_delete_view(self):
        self.client.login(email='testuser', password='testpassword')
        created_material = Material.objects.create(topic='Test Material', text='Test Material',
                                                   chapter_id=self.chapter.pk)
        created_material.save()
        self.client.post(
            reverse('education_content:material_delete', kwargs={'pk': created_material.pk}))

        # Check that the Material object was deleted
        created_material = Material.objects.filter(topic='Test Material', description='Test Material').first()
        self.assertIsNone(created_material)

    def test_material_update_view(self):
        self.client.login(email='testuser', password='testpassword')
        created_material = Material.objects.create(topic='Test Material', text='Test Material',
                                                   chapter_id=self.chapter.pk)
        created_material.save()
        self.client.post(
            reverse('education_content:material_edit', kwargs={'pk': created_material.pk}),
            {'topic': 'Test Material new', 'text': 'Test Material new'})

        # Check that the Material object was deleted
        created_material = Material.objects.filter(topic='Test Material new', text='Test Material new').first()
        self.assertIsNotNone(created_material)

    def test_material_list_view(self):
        self.client.login(email='testuser', password='testpassword')
        response = self.client.get(reverse('education_content:material_list'))
        self.assertEqual(response.status_code, 200)  # Check for a successful response

    def test_material_detail_view(self):
        self.client.login(email='testuser', password='testpassword')
        material = Material.objects.create(topic='Test Material', owner=self.user, chapter=self.chapter)
        response = self.client.get(reverse('education_content:material_view', kwargs={'pk': material.pk}))
        self.assertEqual(response.status_code, 200)  # Check for a successful response


class StatusControllersTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(email='testuser', password='testpassword')
        self.test_object = Chapter.objects.create(title='Test Object')

    def test_change_published_status(self):
        self.client.login(email='testuser', password='testpassword')
        old = self.test_object.is_published
        # Call the change_published_status view
        response = self.client.get(reverse('education_content:change_published_status',
                                           kwargs={'model': 'Chapter', 'pk': self.test_object.pk}))
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect

        # Check that the is_published status has changed in the object
        self.test_object.refresh_from_db()  # Refresh the object from the database
        new = self.test_object.is_published
        self.assertEqual(new, not old)

    def test_change_published_status_for_wrong_request(self):
        self.client.login(email='testuser', password='testpassword')
        # Call the change_published_status view
        response = self.client.get(reverse('education_content:change_published_status',
                                           kwargs={'model': 'Chapter', 'pk': 99999}))
        self.assertEqual(response.status_code, 404)  # Check for 404 error status

    def test_change_published_requested_status(self):
        self.client.login(email='testuser', password='testpassword')
        old = self.test_object.is_published_requested
        # Call the change_published_requested_status view
        response = self.client.get(reverse('education_content:change_published_requested_status',
                                           kwargs={'model': 'Chapter', 'pk': self.test_object.pk}))
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect

        # Check that the is_published_requested status has changed in the object
        self.test_object.refresh_from_db()  # Refresh the object from the database
        new = self.test_object.is_published_requested
        self.assertEqual(new, not old)

    def test_change_published_requested_status_for_wrong_request(self):
        self.client.login(email='testuser', password='testpassword')
        response = self.client.get(reverse('education_content:change_published_requested_status',
                                           kwargs={'model': 'Chapter', 'pk': 999999}))
        self.assertEqual(response.status_code, 404)  # Check for 404 error status

    def test_change_published_requested_status_for_wrong_user(self):
        self.user2 = User.objects.create_user(email='testuser2', password='testpassword2')
        self.client.login(email='testuser2', password='testpassword2')
        response = self.client.get(reverse('education_content:change_published_requested_status',
                                           kwargs={'model': 'Chapter', 'pk': self.test_object.pk}))
        self.assertEqual(response.status_code, 404)  # Check for 404 error status


class MaterialPhotosControllerTests(TestCase):
    def setUp(self):
        # Create a test User
        self.user = User.objects.create_user(email='testuser', password='testpassword')
        # Create a test Chapter
        self.chapter = Chapter.objects.create(title='Test Chapter', owner=self.user, description='Test Chapter')
        # Create a test Material
        self.material = Material.objects.create(topic='Test Material', text='Test Material', chapter=self.chapter)

    def test_material_photos_create_for_special_material_view(self):
        self.client.login(email='testuser', password='testpassword')

        with open('media/kartinki-apelsina-8.jpg', 'rb') as file:
            test_image = SimpleUploadedFile('test_image.jpg', file.read())

        # Call the MaterialPhotosCreateMaterialView view
        response = self.client.post(
            reverse('education_content:materialphotos_create_for_special_material',
                    kwargs={'material_pk': self.material.pk}),
            {'signature': 'Test Image', 'material': self.material.pk, 'figure': test_image})

        self.assertEqual(response.status_code, 302)  # Check for a successful redirect

        # Check that the MaterialPhotos object was created
        created_material_photos = MaterialPhotos.objects.filter(signature='Test Image',
                                                                material=self.material).first()
        self.assertIsNotNone(created_material_photos)

        request = self.client.get(
            reverse('education_content:materialphotos_create_for_special_material',
                    kwargs={'material_pk': self.material.pk}))

        # Check for the 'chapter_pk' parameter in the response context
        self.assertIn('material_pk', request.context)

    def test_material_photos_create_view(self):
        self.client.login(email='testuser', password='testpassword')

        with open('media/kartinki-apelsina-8.jpg', 'rb') as file:
            test_image = SimpleUploadedFile('test_image.jpg', file.read())

        # Call the MaterialPhotosCreateView view
        response = self.client.post(reverse('education_content:materialphotos_create'),
                                    {'signature': 'Test Image', 'material': self.material.pk, 'figure': test_image})

        self.assertEqual(response.status_code, 302)  # Check for a successful redirect

        # Check that the MaterialPhotos object was created
        created_material_photos = MaterialPhotos.objects.filter(signature='Test Image',
                                                                material=self.material).first()
        self.assertIsNotNone(created_material_photos)

        request = self.client.get(
            reverse('education_content:materialphotos_create'))

        # Check for the 'chapter_list' parameter in the response context
        self.assertIn('material_list', request.context)

    def test_material_photos_list_view(self):
        self.client.login(email='testuser', password='testpassword')

        # Call the MaterialPhotosListView view
        response = self.client.get(reverse('education_content:materialphotos_list'))
        self.assertEqual(response.status_code, 200)  # Check for a successful response

    def test_material_photos_detail_view(self):
        self.client.login(email='testuser', password='testpassword')
        material_photos = MaterialPhotos.objects.create(signature='Test Image', material=self.material)

        # Call the MaterialPhotosDetailView view
        response = self.client.get(
            reverse('education_content:materialphotos_view', kwargs={'pk': material_photos.pk}))
        self.assertEqual(response.status_code, 200)  # Check for a successful response

    def test_material_photos_delete_view(self):
        self.client.login(email='testuser', password='testpassword')
        material_photos = MaterialPhotos.objects.create(signature='Test Image', material=self.material)

        # Call the MaterialPhotosDeleteView view
        response = self.client.post(
            reverse('education_content:materialphotos_delete', kwargs={'pk': material_photos.pk}))
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect

        # Check that the MaterialPhotos object was deleted
        deleted_material_photos = MaterialPhotos.objects.filter(signature='Test Image',
                                                                material=self.material).first()
        self.assertIsNone(deleted_material_photos)


class TemplateTagsTestCase(SimpleTestCase):

    def test_mediapath(self):
        result = mediapath("my_image.jpg")
        self.assertEqual(result, '/media/my_image.jpg')

    def test_mediapath_filter(self):
        result = mediapath_filter("my_image.jpg")
        self.assertEqual(result, '/media/my_image.jpg')

    def test_get_item_existing_key(self):
        dictionary = {'key1': 'value1', 'key2': 'value2'}
        result = get_item(dictionary, 'key1')
        self.assertEqual(result, 'value1')

    def test_get_item_non_existing_key(self):
        dictionary = {'key1': 'value1', 'key2': 'value2'}
        result = get_item(dictionary, 'key3')
        self.assertEqual(result, 'Key not found')
