# Generated by Django 3.1.1 on 2021-02-16 12:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_remove_message_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 16, 17, 43, 12, 492160)),
        ),
    ]
