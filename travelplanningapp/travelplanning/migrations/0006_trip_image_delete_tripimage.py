# Generated by Django 5.0.4 on 2024-04-14 13:33

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travelplanning', '0005_alter_tripplan_startlocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='image',
            field=cloudinary.models.CloudinaryField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='TripImage',
        ),
    ]