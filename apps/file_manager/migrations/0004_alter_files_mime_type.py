# Generated by Django 5.2.4 on 2025-07-23 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0003_rename_file_size_files_size_files_uuid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='mime_type',
            field=models.CharField(max_length=150),
        ),
    ]
