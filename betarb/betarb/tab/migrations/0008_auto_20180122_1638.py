# Generated by Django 2.0.1 on 2018-01-22 05:38

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0007_auto_20180122_0327'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='result',
            managers=[
                ('ord_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='result',
            name='runner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tab.Runner'),
        ),
    ]