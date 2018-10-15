# Generated by Django 2.1.2 on 2018-10-15 22:00

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerSeason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('votes_win', models.PositiveIntegerField(default=0, editable=False, verbose_name='votes win')),
                ('votes_tie', models.PositiveIntegerField(default=0, editable=False, verbose_name='votes tie')),
                ('rating_mu', models.FloatField(default=25.0, verbose_name='Rating MU')),
                ('rating_sigma', models.FloatField(default=8.333333333333334, verbose_name='Rating SIGMA')),
                ('pts', models.FloatField(verbose_name='PTS')),
                ('reb', models.FloatField(verbose_name='REB')),
                ('ast', models.FloatField(verbose_name='AST')),
                ('stl', models.FloatField(verbose_name='STL')),
                ('blk', models.FloatField(verbose_name='BLK')),
                ('fg_pct', models.FloatField(verbose_name='FG%')),
                ('fg3_pct', models.FloatField(verbose_name='3P%')),
                ('ft_pct', models.FloatField(verbose_name='FT%')),
                ('ROSTERSTATUS', models.PositiveSmallIntegerField(verbose_name='ROSTERSTATUS')),
                ('GAMES_PLAYED_FLAG', models.CharField(max_length=8, verbose_name='GAMES_PLAYED_FLAG')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='players.Player', verbose_name='player')),
            ],
            options={
                'verbose_name': 'player season',
                'verbose_name_plural': 'player seasons',
                'ordering': ['-season', '-rating_mu', 'rating_sigma'],
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('abbr', models.CharField(max_length=16, verbose_name='season')),
            ],
            options={
                'verbose_name': 'season',
                'verbose_name_plural': 'seasons',
                'ordering': ['-abbr'],
            },
        ),
        migrations.AddField(
            model_name='playerseason',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players_seasons', to='seasons.Season', verbose_name='season'),
        ),
        migrations.AddField(
            model_name='playerseason',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='players_seasons', to='teams.Team', verbose_name='team'),
        ),
        migrations.AlterUniqueTogether(
            name='playerseason',
            unique_together={('player', 'season')},
        ),
    ]
