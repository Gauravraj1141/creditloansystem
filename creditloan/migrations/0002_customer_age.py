# Generated by Django 4.0 on 2024-01-15 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditloan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='age',
            field=models.IntegerField(default=None),
        ),
    ]
