# Generated by Django 4.1.7 on 2023-02-26 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_appuser_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='type_od_user',
            field=models.CharField(blank=True, default='', max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='age',
            field=models.PositiveIntegerField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='gender',
            field=models.CharField(blank=True, default='', max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='height',
            field=models.PositiveIntegerField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='weight',
            field=models.PositiveIntegerField(blank=True, default='', null=True),
        ),
    ]
