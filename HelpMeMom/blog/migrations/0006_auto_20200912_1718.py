# Generated by Django 3.1.1 on 2020-09-12 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_coins'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coins',
            old_name='coins',
            new_name='coinNo',
        ),
    ]
