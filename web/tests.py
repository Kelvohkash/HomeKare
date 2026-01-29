from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from web.models import Category, Service

class HomeKareTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Cleaning", slug="cleaning", icon="fa-broom")
        self.service = Service.objects.create(
            title="House Cleaning",
            description="Deep clean your home",
            category=self.category,
            price=1500
        )

    def test_index_page_rebranding(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HomeKare")
        self.assertContains(response, "House Cleaning")
        self.assertContains(response, "Cleaning")

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Account")

    def test_signup_submission(self):
        signup_data = {
            'username': 'testuser',
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '0712345678',
            'contact_preference': 'email',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
        }
        response = self.client.post(reverse('signup'), signup_data)
        # Should redirect to login on success
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        user = User.objects.get(username='testuser')
        self.assertEqual(user.first_name, 'Test User')
        self.assertEqual(user.profile.phone_number, '0712345678')
