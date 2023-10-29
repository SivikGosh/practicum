# Generated by Django 2.2.16 on 2022-10-18 22:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20221019_0135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='following',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]