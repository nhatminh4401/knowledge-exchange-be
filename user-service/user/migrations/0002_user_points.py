# Generated by Django 4.1.9 on 2023-08-20 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user", name="points", field=models.IntegerField(default=0),
        ),
    ]
