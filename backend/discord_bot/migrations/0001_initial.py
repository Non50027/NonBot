# Generated by Django 5.1.1 on 2024-12-05 14:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('twitch_bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guild', models.CharField(max_length=50)),
                ('member', models.CharField(max_length=50)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RankVoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guild', models.CharField(max_length=50)),
                ('member', models.CharField(max_length=50)),
                ('date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LiveTwitch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guild', models.CharField(max_length=50)),
                ('channel', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=50, null=True)),
                ('twitch_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discord_sub', to='twitch_bot.channel')),
            ],
        ),
    ]
