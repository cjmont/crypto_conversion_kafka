# Generated by Django 4.0.4 on 2022-05-30 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_pay_alter_pendingtransferstatus_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferrequest',
            name='transfer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transactions.transfer', unique=True),
        ),
    ]
