# Generated by Django 4.1 on 2022-12-02 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "organizational_area",
            "0004_organizationalstructure_is_public_engagement_enabled_and_more",
        ),
        (
            "public_engagement_management",
            "0008_alter_publicengagementpartner_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="publicengagementpartner",
            name="partner",
            field=models.ForeignKey(
                limit_choices_to={"is_public_engagement_enabled": True},
                on_delete=django.db.models.deletion.PROTECT,
                to="organizational_area.organizationalstructure",
            ),
        ),
    ]
