# Generated by Django 4.2.5 on 2023-10-29 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_category_description_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorygroup',
            name='enabled',
        ),
    ]
