# Generated by Django 4.0.3 on 2022-06-15 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sheduled_times', models.CharField(max_length=1000)),
                ('bus_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webhook.buses')),
            ],
        ),
    ]