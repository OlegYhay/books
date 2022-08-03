from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from .models import Book


class BookTests(TestCase):
    def setUp(self):
        self.book1 = Book.objects.create(
            title='testbook1',
            author='Oleg Yhay',
            price='25.00',
        )

    def test_list_view(self):
        response = self.client.get(reverse('book_list'))

        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'testbook1')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_detail_view(self):
        url = reverse('book_detail', args=[self.book1.id, ])
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'testbook1')
        self.assertContains(response, '25.00')
        self.assertTemplateUsed(response, 'books/book_detail.html')

    def test_no_detail_and_list_view(self):
        urlDetail = '/books/12345/'
        responsedetail = self.client.get(urlDetail)

        self.assertEqual(404, responsedetail.status_code)
