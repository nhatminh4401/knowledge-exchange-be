# Generated by Django 4.1.9 on 2023-08-23 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_user_about"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="about",
            field=models.CharField(default="", max_length=300),
        ),
    ]
