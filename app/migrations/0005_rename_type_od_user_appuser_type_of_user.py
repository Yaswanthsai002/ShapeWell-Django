# Generated by Django 4.1.7 on 2023-02-26 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_appuser_type_od_user_alter_appuser_age_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appuser',
            old_name='type_od_user',
            new_name='type_of_user',
        ),
    ]
