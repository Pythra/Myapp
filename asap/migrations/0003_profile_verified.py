# Generated by Django 5.1.4 on 2024-12-27 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asap', '0002_alter_profile_user_alter_bank_user_profile_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
