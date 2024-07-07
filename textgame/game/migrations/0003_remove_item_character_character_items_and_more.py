# Generated by Django 5.0.6 on 2024-07-06 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='character',
        ),
        migrations.AddField(
            model_name='character',
            name='items',
            field=models.ManyToManyField(blank=True, to='game.item'),
        ),
        migrations.AddField(
            model_name='character',
            name='money',
            field=models.IntegerField(default=100),
        ),
    ]