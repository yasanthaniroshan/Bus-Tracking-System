# Generated by Django 4.0.3 on 2022-06-25 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_location_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statics_Searching',
            fields=[
                ('key_id', models.AutoField(primary_key=True, serialize=False)),
                ('destination_point', models.CharField(max_length=300)),
                ('starting_point', models.CharField(max_length=200)),
                ('user_location', models.CharField(max_length=200)),
                ('starting_point_to_destination_point', models.BooleanField()),
                ('route_number', models.IntegerField()),
            ],
        ),
    ]
