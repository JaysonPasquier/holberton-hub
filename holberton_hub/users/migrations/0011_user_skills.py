# Generated by Django 5.1.6 on 2025-02-17 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_user_company_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='skills',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
