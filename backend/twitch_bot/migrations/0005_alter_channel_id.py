# Generated by Django 5.1.1 on 2024-12-05 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitch_bot', '0004_alter_channel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]