from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from .models import Book, Review


class BookTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='jadk.fre@mail.ru',
            password='123',
        )
        self.book1 = Book.objects.create(
            title='testbook1',
            author='Oleg Yhay',
            price='25.00',
        )
        self.review1 = Review.objects.create(
            book=self.book1,
            author=self.user,
            review='I like it!'
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
        self.assertContains(response, 'I like it!')
        self.assertTemplateUsed(response, 'books/book_detail.html')

    def test_no_detail_and_list_view(self):
        urlDetail = '/books/12345/'
        responsedetail = self.client.get(urlDetail)

        self.assertEqual(404, responsedetail.status_code)
