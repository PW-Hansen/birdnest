# Generated by Django 4.1.5 on 2023-01-09 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_drone_last_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drone',
            name='last_seen',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
