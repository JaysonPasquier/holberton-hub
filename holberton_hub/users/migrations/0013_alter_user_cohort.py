# Generated by Django 5.1.6 on 2025-02-20 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_user_dev_to_profile_user_gitlab_profile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cohort',
            field=models.CharField(blank=True, choices=[('C#22', 'Cohorte 22'), ('C#23', 'Cohorte 23'), ('C#24', 'Cohorte 24'), ('C#25', 'Cohorte 25'), ('C#26', 'Cohorte 26')], max_length=10, null=True),
        ),
    ]
