# Generated by Django 2.2 on 2021-04-19 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchApp', '0009_auto_20210418_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
