# Generated by Django 2.0.1 on 2018-02-09 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betfair', '0025_auto_20180209_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='bets_status',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
