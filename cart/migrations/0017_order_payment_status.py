# Generated by Django 3.2.6 on 2021-10-09 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0016_alter_cart_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('NEW', 'NEW'), ('PENDING', 'PENDING'), ('CANCELED', 'CANCELED'), ('COMPLETED', 'COMPLETED')], default='NEW', max_length=9),
        ),
    ]
