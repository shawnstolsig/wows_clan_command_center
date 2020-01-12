# Generated by Django 3.0 on 2020-01-12 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Upgrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upgrade_id', models.IntegerField()),
                ('upgrade_name', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ship_id', models.IntegerField()),
                ('ship_name', models.CharField(max_length=50)),
                ('ship_class', models.CharField(max_length=2)),
                ('ship_tier', models.IntegerField()),
                ('ship_nation', models.CharField(max_length=50)),
                ('ship_upgrade_slots', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('ship_upgrades', models.ManyToManyField(related_name='ship_upgrades', to='data.Upgrade')),
            ],
        ),
    ]