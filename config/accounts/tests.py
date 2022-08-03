from django.test import TestCase
from django.urls import reverse, resolve

from .forms import CustomUserCreationForm


class SigUpTests(TestCase):
    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')

    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertContains(self.response, 'csrfmiddlewaretoken')



