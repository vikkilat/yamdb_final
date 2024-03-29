# Generated by Django 3.2 on 2023-03-01 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id'], 'verbose_name': 'Пользователь.', 'verbose_name_plural': 'Пользователи.'},
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, help_text='Краткая информация о пользователе.', verbose_name='Дополнительная информация.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.SlugField(blank=True, help_text='Проверочный код для регистрации на сайте.', null=True, verbose_name='Код.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text='Адрес электронной почты пользователя.', max_length=254, unique=True, verbose_name='E-mail.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, help_text='Имя пользователя.', max_length=150, verbose_name='Имя.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, help_text='Фамилия пользователя.', max_length=150, verbose_name='Фамилия.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.SlugField(choices=[('user', 'Аутентифицированный пользователь'), ('admin', 'Админ'), ('moderator', 'Модератор')], default='user', help_text='Роль присвоенная пользователю на данном ресурсе.', verbose_name='Роль.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.SlugField(help_text='Ник пользователя.', max_length=150, unique=True, verbose_name='Ник пользователя.'),
        ),
    ]
