# Generated by Django 3.2.6 on 2021-10-09 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0018_order_status_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='paid',
        ),
    ]
