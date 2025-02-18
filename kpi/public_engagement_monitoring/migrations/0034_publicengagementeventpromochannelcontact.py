# Generated by Django 5.1.4 on 2025-02-18 14:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizational_area', '0006_alter_organizationalstructure_options'),
        ('public_engagement_monitoring', '0033_rename_person_publicengagementeventdata_involved_personnel_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicEngagementEventPromoChannelContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
                ('promo_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public_engagement_monitoring.publicengagementeventpromochannel', verbose_name='Contact')),
                ('structure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizational_area.organizationalstructure', verbose_name='Structure')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
