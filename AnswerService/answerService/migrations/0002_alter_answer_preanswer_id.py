# Generated by Django 4.1.9 on 2023-08-25 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answerService', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='preAnswer_ID',
            field=models.IntegerField(null=True),
        ),
    ]
