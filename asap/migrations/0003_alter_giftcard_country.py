# Generated by Django 5.1.4 on 2025-03-02 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asap', '0002_crypto_remove_giftcard_category_remove_giftcard_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftcard',
            name='country',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
