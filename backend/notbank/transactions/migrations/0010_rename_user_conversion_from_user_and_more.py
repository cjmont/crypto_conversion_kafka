# Generated by Django 4.0.4 on 2022-06-08 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0009_conversion_task_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conversion',
            old_name='user',
            new_name='from_user',
        ),
        migrations.RemoveField(
            model_name='conversion',
            name='amount',
        ),
        migrations.AddField(
            model_name='conversion',
            name='from_amount',
            field=models.DecimalField(decimal_places=18, default=0, max_digits=36),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conversion',
            name='to_amount',
            field=models.DecimalField(decimal_places=18, default=0, max_digits=36),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='conversion',
            name='status',
            field=models.IntegerField(choices=[(0, 'Éxito'), (1, 'Error'), (2, 'Pendiente')], default=0),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='status',
            field=models.IntegerField(choices=[(0, 'Éxito'), (1, 'Error'), (2, 'Pendiente')], default=0),
        ),
    ]
