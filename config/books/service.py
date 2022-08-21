from django.core.mail import send_mail


def send_mails(user_mail,pk):
    send_mail(f'Вы только что оформили заказ №{pk} на сайте bookstore',
              'С вам в течение дня свяжется наш менеджер! Спасибо что выбрали нас',
              'olesya198fwaefawfawf@gmail.com',
              [user_mail],
              fail_silently=False,)
