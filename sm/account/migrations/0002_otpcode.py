# Generated by Django 5.0 on 2025-07-11 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtpCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11)),
                ('code', models.PositiveSmallIntegerField()),
                ('created', models.DateField(auto_now=True)),
            ],
        ),
    ]
