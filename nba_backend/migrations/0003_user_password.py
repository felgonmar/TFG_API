# Generated by Django 3.2 on 2023-05-11 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba_backend', '0002_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]