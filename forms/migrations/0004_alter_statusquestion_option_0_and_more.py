# Generated by Django 4.2.5 on 2023-09-23 12:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forms", "0003_alter_eventquestion_date_alter_eventquestion_event_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="statusquestion",
            name="option_0",
            field=models.CharField(blank=True, default="Off", max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="statusquestion",
            name="option_1",
            field=models.CharField(blank=True, default="On", max_length=10, null=True),
        ),
    ]
