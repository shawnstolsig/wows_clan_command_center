# Generated by Django 3.0 on 2020-01-12 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20200112_0137'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='skill_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]