# Generated by Django 3.2.6 on 2021-09-09 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_sizes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='sizes',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.product'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sizes',
            name='size_type',
            field=models.CharField(choices=[('EU 35-37', 'EU 35-37'), ('EU 38-40', 'EU 38-40'), ('EU 41-43', 'EU 41-43')], max_length=128),
        ),
    ]
