# Generated by Django 2.1.2 on 2019-01-22 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190119_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='can_drive',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='glidingsession',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
    ]
