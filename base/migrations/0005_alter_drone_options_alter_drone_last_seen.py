# Generated by Django 4.1.5 on 2023-01-16 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_drone_last_seen'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drone',
            options={'ordering': ['last_seen']},
        ),
        migrations.AlterField(
            model_name='drone',
            name='last_seen',
            field=models.DateTimeField(),
        ),
    ]