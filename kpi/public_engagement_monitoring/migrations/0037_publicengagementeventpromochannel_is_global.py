# Generated by Django 5.1.4 on 2025-02-18 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_engagement_monitoring', '0036_alter_publicengagementeventpromochannelcontact_structure'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicengagementeventpromochannel',
            name='is_global',
            field=models.BooleanField(default=True),
        ),
    ]
