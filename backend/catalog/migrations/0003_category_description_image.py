# Generated by Django 4.2.5 on 2023-10-29 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_category_enabled_categorygroup_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]