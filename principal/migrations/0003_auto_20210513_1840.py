# Generated by Django 3.1.7 on 2021-05-13 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0002_auto_20210513_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vino',
            name='tiposUva',
        ),
        migrations.AddField(
            model_name='vino',
            name='tiposUva',
            field=models.ManyToManyField(to='principal.TipoUva'),
        ),
    ]
