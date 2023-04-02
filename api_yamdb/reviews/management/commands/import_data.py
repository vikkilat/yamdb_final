from csv import DictReader

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

TABLES_DICT = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    """Импорт данных в БД."""
    help = 'Load data from csv files'

    def handle(self, *args, **kwargs):
        for model, base in TABLES_DICT.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{base}',
                'r', encoding='utf-8'
            ) as csv_file:
                reader = DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)

        self.stdout.write(self.style.SUCCESS('Successfully load data'))

    def import_genre_title(self):
        """Импорт данных в БД для genre_title."""
        for row in DictReader(open(settings.CSV_DIR / 'genre_title.csv',
                                   encoding='utf8')):
            Title.genre.through.create(
                id=row['id'],
                title_id=row['title_id'],
                genre_id=row['genre_id'],
            )
        print('Successfully load data Genre_title')


"""
Менеджмент команда работает, порядок заполнения вроде логически верный,
но при заполнении модели Title ругается на отсутствие категории (которая
заполнена раньше. Накатывал несколько раз на пустую БД, заполнение проверял...
"""
