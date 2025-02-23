# Generated by Django 5.0.1 on 2024-01-23 13:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField(default=datetime.datetime.today)),
                ('booking_time', models.TimeField(null=True)),
                ('book_time', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Futsal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('images', models.ImageField(default='football-bg.jpg', upload_to='')),
                ('futsal_type', models.CharField(choices=[('5A', '5-A-Side'), ('7A', '7-A-Side'), ('6A', '6-A-Side')], max_length=2)),
                ('location', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('open_time', models.TimeField()),
                ('close_time', models.TimeField()),
                ('contact_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
