# Generated by Django 3.2.6 on 2021-09-29 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='device',
            new_name='client',
        ),
    ]
