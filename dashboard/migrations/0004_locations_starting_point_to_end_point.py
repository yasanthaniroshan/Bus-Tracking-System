# Generated by Django 4.0.3 on 2022-06-22 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_gettinglocations'),
    ]

    operations = [
        migrations.AddField(
            model_name='locations',
            name='starting_point_to_end_point',
            field=models.CharField(default='', max_length=10000),
        ),
    ]