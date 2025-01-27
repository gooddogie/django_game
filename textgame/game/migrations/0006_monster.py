# Generated by Django 5.0.6 on 2024-07-07 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_item_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('level', models.IntegerField(default=1)),
                ('experience_worth', models.IntegerField(default=0)),
                ('hp', models.IntegerField(default=10)),
                ('armor', models.IntegerField(default=1)),
                ('power', models.IntegerField(default=5)),
            ],
        ),
    ]
