# Generated by Django 4.1.9 on 2023-08-20 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionService', '0005_alter_question_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='user',
            field=models.IntegerField(),
        ),
    ]
