# Generated by Django 4.1 on 2022-12-20 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("visiting_management", "0014_alter_visiting_from_structure_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collaboration",
            name="collab_type",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="role",
            name="role_type",
            field=models.CharField(max_length=255),
        ),
    ]
