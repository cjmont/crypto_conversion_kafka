# Generated by Django 4.0.4 on 2022-05-30 18:17

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_pendingtransferstatus_transfer_remove_user_user_uuid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('active', models.BooleanField(default=True)),
                ('from_user', models.CharField(max_length=32, null=True)),
                ('to_user', models.CharField(max_length=32, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='pendingtransferstatus',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='pendingtransferstatus',
            name='task_ID',
            field=models.CharField(max_length=300, unique=True),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='task_ID',
            field=models.CharField(max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='transferrequest',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transferrequest',
            name='task_ID',
            field=models.CharField(max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
    ]
