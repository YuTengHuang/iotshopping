# Generated by Django 5.0.3 on 2024-04-17 13:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ('related_member',)},
        ),
        migrations.RenameField(
            model_name='address',
            old_name='member_id',
            new_name='related_member',
        ),
        migrations.AddField(
            model_name='member',
            name='related_address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='member.address'),
        ),
    ]
