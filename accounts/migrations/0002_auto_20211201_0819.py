# Generated by Django 3.2.9 on 2021-12-01 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bod',
            field=models.CharField(choices=[('Y', 'BOD'), ('N', 'Non BOD')], max_length=1, null=True, verbose_name='Status BOD ?'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], max_length=1, null=True, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]