# Generated by Django 3.1.3 on 2021-01-19 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0011_auto_20210112_2033'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='weeek_days',
            new_name='week_days',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='valid_till',
        ),
        migrations.AddField(
            model_name='schedule',
            name='valid_untill',
            field=models.DateField(default=None, verbose_name='valid untill'),
        ),
    ]
