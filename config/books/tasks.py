from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from config.celery import app
from .service import send_mails


@app.task
def send_spam_email(user_email, pk):
    send_mails(user_email, pk)


@app.task
def send_spam_every_1_minute():
    for user in get_user_model().objects.all():
        send_mail(f'Этот спам с сайте bookstore',
                  'Купите что нибудь и мы дадим вам может быть скидку',
                  'olesya198fwaefawfawf@gmail.com',
                  [user.email],
                  fail_silently=False,)

