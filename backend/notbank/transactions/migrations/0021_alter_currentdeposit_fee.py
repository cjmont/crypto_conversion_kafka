# Generated by Django 4.0.4 on 2022-07-29 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0020_currentdeposit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentdeposit',
            name='fee',
            field=models.DecimalField(decimal_places=18, max_digits=36, null=True),
        ),
    ]
