# Generated by Django 3.2.9 on 2021-11-23 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pica', '0010_alter_signature_lines'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='due_date',
            field=models.DateField(blank=True, null=True, verbose_name='New Due Date (If Any)'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='status',
            field=models.CharField(choices=[('OPEN', 'OPEN'), ('CLOSE', 'CLOSE')], default='OPEN', max_length=8),
        ),
    ]
