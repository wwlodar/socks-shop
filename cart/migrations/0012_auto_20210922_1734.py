# Generated by Django 3.2.6 on 2021-09-22 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        ('cart', '0011_auto_20210922_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clients.client'),
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clients.client'),
        ),
    ]