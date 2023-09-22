# Generated by Django 4.2.5 on 2023-09-22 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authuser", "0002_alter_clinician_patients_alter_patient_dob_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clinician",
            name="patients",
            field=models.ManyToManyField(
                blank=True, related_name="clinicians", to="authuser.patient"
            ),
        ),
    ]