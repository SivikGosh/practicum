import os
import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import User
from titles.models import Title, Genre, Category, GenreTitle
from reviews.models import Review, Comment

models = {
    User: 'static/data/users.csv',
    Category: 'static/data/category.csv',
    Genre: 'static/data/genre.csv',
    Title: 'static/data/titles.csv',
    Review: 'static/data/review.csv',
    Comment: 'static/data/comments.csv',
    GenreTitle: 'static/data/genre_title.csv',
}


class Command(BaseCommand):
    """Импорт данных из csv файлов в таблицы БД."""

    help = 'Imports data from csv files into the database.'

    def handle(self, *args, **kwargs):
        for model, path in models.items():
            with open(os.path.join(settings.BASE_DIR, path),
                      encoding='utf8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                model.objects.all().delete()
                model_obj = []

                if model == Title:
                    for row in reader:
                        category = Category.objects.get(id=row['category'])
                        model_ = model(
                            id=row['id'],
                            name=row['name'],
                            year=row['year'],
                            category=category
                        )
                        model_obj.append(model_)

                elif model == Review:
                    for row in reader:
                        title_id = Title.objects.get(id=row['title_id'])
                        author = User.objects.get(id=row['author'])
                        model_ = model(
                            id=row['id'],
                            title=title_id,
                            text=row['text'],
                            author=author,
                            score=row['score'],
                            pub_date=row['pub_date']
                        )
                        model_obj.append(model_)

                elif model == Comment:
                    for row in reader:
                        review_id = Review.objects.get(id=row['review_id'])
                        author = User.objects.get(id=row['author'])
                        model_ = model(
                            id=row['id'],
                            review_id=review_id,
                            text=row['text'],
                            author=author,
                            pub_date=row['pub_date']
                        )
                        model_obj.append(model_)

                else:
                    for row in reader:
                        model_ = model(**row)
                        model_obj.append(model_)

                model.objects.bulk_create(model_obj)
