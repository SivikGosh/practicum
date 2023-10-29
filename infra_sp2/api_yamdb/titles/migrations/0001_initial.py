# Generated by Django 2.2.16 on 2022-11-10 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название категории', max_length=256, verbose_name='Название')),
                ('slug', models.SlugField(help_text='Адрес категории в адресной строке', unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название жанра', max_length=256, verbose_name='Название')),
                ('slug', models.SlugField(help_text='Адрес жанра в адресной строке', unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='titles.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название произведения', max_length=100, verbose_name='Название')),
                ('year', models.PositiveSmallIntegerField(help_text='Год выпуска произведения', verbose_name='Год выпуска')),
                ('description', models.TextField(help_text='Описание произведения', verbose_name='Описание')),
                ('category', models.ForeignKey(help_text='Категория произведения', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='titles.Category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(related_name='titles', through='titles.GenreTitle', to='titles.Genre')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='genretitle',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='titles.Title'),
        ),
    ]