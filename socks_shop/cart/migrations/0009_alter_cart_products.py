# Generated by Django 3.2.6 on 2021-09-02 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_alter_cart_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(to='cart.OrderedProduct'),
        ),
    ]
