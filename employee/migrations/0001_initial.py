# Generated by Django 4.2 on 2023-05-06 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('address', models.CharField(max_length=200)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cities_light.city')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', models.CharField(max_length=20, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('year', models.IntegerField()),
                ('doors', models.PositiveSmallIntegerField()),
                ('seats', models.PositiveSmallIntegerField()),
                ('ac', models.BooleanField()),
                ('gearbox', models.CharField(choices=[('AT', 'Automatic'), ('MT', 'Manual')], max_length=2)),
                ('fuel', models.CharField(choices=[('G', 'Gasoline'), ('D', 'Diesel'), ('H', 'Hybrid'), ('E', 'Electric')], max_length=1)),
                ('picture', models.ImageField(default='cars/default.png', upload_to='cars/')),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='employee.agency')),
            ],
        ),
        migrations.CreateModel(
            name='CarBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('rental_price', models.FloatField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('paid', models.BooleanField(default=False)),
                ('confirmed', models.BooleanField(default=False)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.car')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('car_model_price', models.FloatField()),
                ('car_brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='employee.carbrand')),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='car_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='employee.carmodel'),
        ),
    ]
