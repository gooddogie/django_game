# Generated by Django 5.0.6 on 2024-07-07 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_character_default_hp_character_stamina_item_stamina_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='monster',
            name='default_hp',
            field=models.IntegerField(default=10),
        ),
    ]
