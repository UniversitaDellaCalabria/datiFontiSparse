# Generated by Django 4.0.3 on 2022-04-06 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizational_area', '0002_organizationalstructure_is_internal'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organizationalstructureoffice',
            options={'ordering': ['name', 'organizational_structure__name'],
                     'verbose_name': 'Organizational Structure Office', 'verbose_name_plural': 'Organizational Structure Offices'},
        ),
    ]
