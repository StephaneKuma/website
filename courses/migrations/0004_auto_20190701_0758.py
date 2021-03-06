# Generated by Django 2.2.2 on 2019-07-01 07:58

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20190629_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='content',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='Content of the lesson'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(default='default.png', upload_to='', verbose_name='course image'),
        ),
    ]
