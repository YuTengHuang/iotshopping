# Generated by Django 4.2.11 on 2024-04-24 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_order_order_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
