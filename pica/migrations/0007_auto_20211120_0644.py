# Generated by Django 3.2.9 on 2021-11-19 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pica', '0006_auto_20211116_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signature',
            name='nama_bod',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='signature',
            name='title',
            field=models.CharField(max_length=20),
        ),
    ]
