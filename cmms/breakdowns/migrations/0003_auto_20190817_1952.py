# Generated by Django 2.2.4 on 2019-08-17 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breakdowns', '0002_machine_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='name',
            field=models.TextField(default='', unique=True),
        ),
    ]