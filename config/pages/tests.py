from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse, resolve

from .views import HomePageView, AboutPageView


class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='will',
            email='will@mail.com',
            password='testpass123'
        )

        self.assertEqual(user.username, 'will')
        self.assertEqual(user.email, 'will@mail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username='will2',
            email='will2@mail.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'will2')
        self.assertEqual(user.email, 'will2@mail.com')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)


class HomePageTests(TestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_url(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_url_resolves(self):
        view = resolve('/')
        print(view)
        self.assertEqual(
            view.func.__name__,
            HomePageView.as_view().__name__
        )


class AboutPageTests(TestCase):

    def setUp(self):
        url = reverse('about')
        self.response = self.client.get(url)

    def test_aboutpage_statuscode(self):
        self.assertEqual(self.response.status_code, 200)

    def test_aboutpage_template(self):
        self.assertTemplateUsed(self.response, 'about.html')

    def test_aboutpage_view(self):
        view = resolve('/about/')
        self.assertEqual(view.func.__name__,
                         AboutPageView.as_view().__name__)

    def test_about_page_content(self):
        self.assertContains(self.response, 'About page')
