# Generated by Django 3.2 on 2023-02-27 00:54

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Категория к которой относится произведение.', max_length=256, unique=True, verbose_name='Категория.')),
                ('slug', models.SlugField(help_text='Имя категории для формирования url.', unique=True, verbose_name='Адрес категории.')),
            ],
            options={
                'verbose_name': 'Категория.',
                'verbose_name_plural': 'Категории.',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Жанр, к которому относятся произведения.', max_length=256, unique=True, verbose_name='Жанр.')),
                ('slug', models.SlugField(help_text='Имя жанра для формирования url.', unique=True, verbose_name='Адрес жанра.')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры.',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('score', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Рейтинг')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название произведения.', max_length=200, unique=True, verbose_name='Произведение.')),
                ('year', models.IntegerField(help_text='Год создания произведения', validators=[django.core.validators.MaxValueValidator(limit_value=2023)], verbose_name='Год.')),
                ('description', models.CharField(blank=True, help_text='Описание произведения.', max_length=300, null=True, verbose_name='Описание.')),
                ('category', models.ForeignKey(blank=True, help_text='Категория произведения.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='Категория.')),
                ('genre', models.ManyToManyField(help_text='Жанры, к которым относится произведение.', to='reviews.Genre', verbose_name='Жанр.')),
            ],
            options={
                'verbose_name': 'Произведение.',
                'verbose_name_plural': 'Произведения.',
            },
        ),
    ]
