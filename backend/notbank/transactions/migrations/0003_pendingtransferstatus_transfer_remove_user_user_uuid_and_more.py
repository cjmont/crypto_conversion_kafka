# Generated by Django 4.0.4 on 2022-05-27 16:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_balancetransfer_charge_user_firebase_id_user_phone_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingTransferStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('active', models.BooleanField(default=True)),
                ('task_ID', models.CharField(max_length=300)),
                ('status', models.IntegerField(choices=[(0, 'Éxito'), (1, 'Error')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('active', models.BooleanField(default=True)),
                ('task_ID', models.CharField(max_length=36)),
                ('currency', models.CharField(max_length=8)),
                ('amount', models.DecimalField(decimal_places=18, max_digits=36)),
                ('fee_amount', models.DecimalField(decimal_places=18, max_digits=36)),
                ('status', models.IntegerField(choices=[(0, 'Éxito'), (1, 'Error'), (2, 'Pendiente')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_UUID',
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.RenameModel(
            old_name='Charge',
            new_name='TransferRequest',
        ),
        migrations.DeleteModel(
            name='BalanceTransfer',
        ),
        migrations.AddField(
            model_name='transfer',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='from_user', to='transactions.user'),
        ),
        migrations.AddField(
            model_name='transfer',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='to_user', to='transactions.user'),
        ),
        migrations.AlterField(
            model_name='transferrequest',
            name='transfer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transactions.transfer'),
        ),
    ]