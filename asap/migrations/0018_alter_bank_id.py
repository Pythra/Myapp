# Generated by Django 5.1.4 on 2025-01-11 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asap', '0017_crypto_alter_notification_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]
