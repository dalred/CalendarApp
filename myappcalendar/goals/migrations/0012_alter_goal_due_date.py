# Generated by Django 4.0.4 on 2022-06-26 10:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0011_alter_goalcategory_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='due_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата дедлайна'),
        ),
    ]