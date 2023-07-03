# Generated by Django 4.0.4 on 2022-08-22 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0021_alter_currentdeposit_fee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='currentdeposit',
            old_name='request_id',
            new_name='task_id',
        ),
        migrations.RemoveField(
            model_name='currentdeposit',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='currentdeposit',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='currentdeposit',
            name='fee',
        ),
    ]