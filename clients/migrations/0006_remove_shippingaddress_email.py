# Generated by Django 3.2.6 on 2021-10-08 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_alter_shippingaddress_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='email',
        ),
    ]
