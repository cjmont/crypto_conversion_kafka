# Generated by Django 4.0.4 on 2022-06-07 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0008_conversion_pendingtransactionstatus_delete_pay_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversion',
            name='task_ID',
            field=models.CharField(default='f636cfc7-c937-4e73-91cb-8e49fd7179ef', max_length=36, unique=True),
            preserve_default=False,
        ),
    ]
