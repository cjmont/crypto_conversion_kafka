# Generated by Django 4.0.4 on 2022-05-31 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_alter_transferrequest_transfer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='firebase_ID',
            new_name='firebase_token',
        ),
        migrations.AddField(
            model_name='transfer',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
