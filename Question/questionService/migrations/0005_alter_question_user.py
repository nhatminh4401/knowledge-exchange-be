# Generated by Django 4.1.9 on 2023-08-18 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionService', '0004_referencelink_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='user',
            field=models.IntegerField(max_length=50),
        ),
    ]
