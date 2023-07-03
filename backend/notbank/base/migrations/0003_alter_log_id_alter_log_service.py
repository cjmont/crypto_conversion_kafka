# Generated by Django 4.0.4 on 2022-07-11 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_log_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='log',
            name='service',
            field=models.TextField(choices=[('SERVER', 'SERVER'), ('KAFKA_CONSUMER', 'KAFKA CONSUMER'), ('CELERY', 'CELERY'), ('KAFKA_PRODUCER', 'KAFKA PRODUCER (called from server or celery)'), ('DELETE_OLD_QUOTE_CRON', 'delete old quotes')]),
        ),
    ]