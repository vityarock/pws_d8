# Generated by Django 3.2.6 on 2021-09-16 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_delete_prioritycount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='priority',
            field=models.CharField(choices=[(1, 'Высокий приоритет'), (2, 'Средний приоритет'), (3, 'Низкий приоритет')], default=2, max_length=2, verbose_name='Приоритет'),
        ),
    ]
