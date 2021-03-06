# Generated by Django 2.1.4 on 2018-12-06 10:40

import ckeditor_uploader.fields
from django.db import migrations, models
import hitcount.models
import snippets.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=125)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('image', models.ImageField(blank=True, upload_to=snippets.models.generate_filename, verbose_name='Фото')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Сниппет',
                'verbose_name_plural': 'Сниппеты',
            },
            bases=(models.Model, hitcount.models.HitCountMixin),
        ),
    ]
