# Generated by Django 5.1.6 on 2025-02-14 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_specialty'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_bot',
            field=models.BooleanField(default=False),
        ),
    ]
