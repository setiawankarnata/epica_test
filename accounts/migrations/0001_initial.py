# Generated by Django 3.2.9 on 2021-11-11 21:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pica', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, default='images/User1.svg', null=True, upload_to='images/')),
                ('gender', models.CharField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], max_length=1, verbose_name='Gender')),
                ('mobile_number', models.CharField(blank=True, max_length=12)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('bod', models.CharField(choices=[('Y', 'BOD'), ('N', 'Non BOD')], max_length=1, verbose_name='Status BOD ?')),
                ('profile2divdept', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pica.divdept', verbose_name='Div/Dept')),
                ('profile2user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user2profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
