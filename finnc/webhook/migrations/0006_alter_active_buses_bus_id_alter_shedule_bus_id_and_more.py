# Generated by Django 4.0.3 on 2022-06-15 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0005_alter_active_buses_bus_id_alter_shedule_bus_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='active_buses',
            name='bus_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webhook.buses'),
        ),
        migrations.AlterField(
            model_name='shedule',
            name='bus_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webhook.buses'),
        ),
        migrations.AlterField(
            model_name='turn_of_bus',
            name='bus_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webhook.buses'),
        ),
    ]
