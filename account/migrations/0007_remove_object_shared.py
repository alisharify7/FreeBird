# Generated by Django 5.0.6 on 2024-07-11 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_object_path_alter_object_sharedto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='shared',
        ),
    ]
