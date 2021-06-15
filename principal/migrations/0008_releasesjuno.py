# Generated by Django 3.2 on 2021-06-14 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0007_rename_releasebeatport_releasesbeatport'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReleasesJuno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.TextField(verbose_name='Artist')),
                ('catalog_number', models.TextField(verbose_name='Catalog Number')),
                ('title', models.TextField(verbose_name='Title')),
                ('year', models.TextField(verbose_name='Year')),
                ('image', models.TextField(verbose_name='Image')),
            ],
            options={
                'ordering': ('-year',),
            },
        ),
    ]