# Generated by Django 5.1.4 on 2025-02-18 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visiting_management', '0015_alter_collaboration_collab_type_alter_role_role_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaboration',
            name='collab_type',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='role',
            name='role_type',
            field=models.CharField(max_length=254),
        ),
    ]
