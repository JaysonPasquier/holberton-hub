# Generated by Django 5.1.6 on 2025-02-14 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0007_user_company_bio_user_company_website'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['is_company'], name='users_user_is_comp_c35a89_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email'], name='users_user_email_6f2530_idx'),
        ),
    ]
