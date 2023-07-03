# Generated by Django 4.0.4 on 2022-06-22 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='service',
            field=models.TextField(choices=[('SERVER', 'SERVER'), ('KAFKA_CONSUMER', 'KAFKA CONSUMER'), ('CELERY', 'CELERY'), ('KAFKA_PRODUCER', 'KAFKA PRODUCER (called from server or celery)')]),
        ),
    ]