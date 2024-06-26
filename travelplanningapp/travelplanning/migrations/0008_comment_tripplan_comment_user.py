# Generated by Django 5.0.4 on 2024-04-20 12:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelplanning', '0007_remove_comment_tripplan_remove_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='tripplan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='travelplanning.tripplan'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
