# Generated by Django 5.1.4 on 2025-02-14 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_engagement_monitoring', '0031_publicengagementeventdata_structures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='description',
            field=models.TextField(help_text='This text will be used for any promotion on institutional channels. Max 1500 chars', max_length=1500, verbose_name='Short description'),
        ),
    ]
