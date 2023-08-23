# Generated by Django 4.1.9 on 2023-08-18 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionService', '0003_alter_question_updated_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferenceLink',
            fields=[
                ('ref_ID', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=500)),
                ('question_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionService.question')),
            ],
            options={
                'verbose_name': 'Reference link',
                'verbose_name_plural': 'Reference links',
                'db_table': 'referencelink',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('img_ID', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=500)),
                ('question_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionService.question')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'db_table': 'image',
            },
        ),
    ]