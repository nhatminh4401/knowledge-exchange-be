# Generated by Django 4.1.9 on 2023-08-16 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionService', '0002_alter_question_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='updated_date',
            field=models.DateTimeField(null=True),
        ),
    ]
