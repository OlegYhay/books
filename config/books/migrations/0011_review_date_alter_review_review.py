# Generated by Django 4.1 on 2022-08-09 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_remove_book_author_link_alter_book_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.CharField(max_length=255, verbose_name='Комментарий'),
        ),
    ]
