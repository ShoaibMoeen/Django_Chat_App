# Generated by Django 3.1.1 on 2021-02-16 12:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_auto_20210216_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 16, 17, 45, 32, 510322)),
        ),
    ]
