# Generated by Django 3.2.6 on 2021-10-08 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20210924_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='email',
            field=models.EmailField(default='user@google.com', max_length=254, unique=False),
            preserve_default=False,
        ),
    ]
