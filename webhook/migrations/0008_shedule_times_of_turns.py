# Generated by Django 4.0.3 on 2022-06-18 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0007_active_buses_active_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='shedule',
            name='times_of_turns',
            field=models.CharField(default='00:00', max_length=1000),
            preserve_default=False,
        ),
    ]
