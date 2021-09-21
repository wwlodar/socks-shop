# Generated by Django 3.2.6 on 2021-09-09 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20210909_2004'),
        ('cart', '0009_alter_cart_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderedproduct',
            name='product',
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='product_in_size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.sizes'),
        ),
    ]
