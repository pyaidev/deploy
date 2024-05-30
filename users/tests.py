from django.test import TestCase
from django.urls import reverse
from users.models import User, CustomUserManager


class RegisterViewTest(TestCase):
    def test_register_view(self):
        # Create a user data dictionary to simulate form input
        user_data = {
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'test@example.com',
        }

        # Use reverse to get the URL for the RegisterView
        url = reverse('users:register')

        # Send a POST request with user data to the RegisterView
        response = self.client.post(url, data=user_data)

        # Check if the user was created and the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())


class ProfileViewTest(TestCase):
    def setUp(self):
        # Create a user and log in
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.client.login(email='test@example.com', password='testpassword')
        self.user_manager = CustomUserManager()

    def test_create_user_with_empty_email(self):
        with self.assertRaises(ValueError) as context:
            self.user_manager.create_user(email='', password='password')
        self.assertEqual(str(context.exception), 'Email is required')

    def test_create_superuser_with_invalid_is_staff(self):
        with self.assertRaises(ValueError) as context:
            self.user_manager.create_superuser(email='admin@example.com', password='password', is_staff=False)
        self.assertEqual(str(context.exception), 'Superuser must have is_staff=True.')

    def test_create_superuser_with_invalid_is_superuser(self):
        with self.assertRaises(ValueError) as context:
            self.user_manager.create_superuser(email='admin@example.com', password='password', is_superuser=False)
        self.assertEqual(str(context.exception), 'Superuser must have is_superuser=True.')

    def test_profile_view(self):
        # Use reverse to get the URL for the ProfileView
        url = reverse('users:profile')

        # Send a GET request to the ProfileView
        response = self.client.get(url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        # Use reverse to get the URL for the ProfileView
        url = reverse('users:profile')

        # Create user data dictionary to simulate form input
        user_data = {
            'password1': 'newpassword',
            'password2': 'newpassword',
            'email': 'updated@example.com',
        }

        # Send a POST request with user data to update the profile
        response = self.client.post(url, data=user_data)

        # Check if the user's profile was updated and the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()  # Refresh the user from the database
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertTrue(self.user.check_password('newpassword'))


class LoginModifiedViewTest(TestCase):
    def test_login_modified_view(self):
        # Create a user data dictionary to simulate form input
        user_data = {
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'test@example.com',
        }

        # Use reverse to get the URL for the RegisterView
        url = reverse('users:register')

        # Send a POST request with user data to the RegisterView
        response = self.client.post(url, data=user_data)

        # Use reverse to get the URL for the LoginModifiedView
        url = reverse('users:login')

        # Send a POST request with login data
        response = self.client.post(url, data={'username': 'test@example.com', 'password': 'testpassword'})

        # Check if the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
