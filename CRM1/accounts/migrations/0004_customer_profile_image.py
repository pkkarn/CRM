# Generated by Django 3.0.8 on 2020-08-07 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_image',
            field=models.ImageField(default='images/default.png', upload_to='images/'),
        ),
    ]
