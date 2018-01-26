# Generated by Django 2.0.1 on 2018-01-25 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0013_race_has_results'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accuracy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('win_dec', models.FloatField()),
                ('win_perc', models.FloatField()),
                ('won', models.BooleanField()),
                ('tab_win_error', models.FloatField()),
                ('place_dec', models.FloatField()),
                ('place_perc', models.FloatField()),
                ('place', models.BooleanField()),
                ('tab_place_error', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='race',
            name='has_processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='accuracy',
            name='race',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tab.Race'),
        ),
        migrations.AddField(
            model_name='accuracy',
            name='runner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tab.Runner'),
        ),
    ]
