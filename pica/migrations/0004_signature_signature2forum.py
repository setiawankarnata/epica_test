# Generated by Django 3.2.9 on 2021-11-15 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pica', '0003_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='signature',
            name='signature2forum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='forum2signature', to='pica.forum', verbose_name='Forum'),
        ),
    ]