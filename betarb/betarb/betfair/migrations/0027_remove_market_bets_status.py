# Generated by Django 2.0.1 on 2018-02-09 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('betfair', '0026_market_bets_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='market',
            name='bets_status',
        ),
    ]
