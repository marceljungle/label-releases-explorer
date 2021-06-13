# encoding:utf-8
from django.db import models

# Create your models here.


class ReleasesBeatport(models.Model):
    artist = models.TextField(verbose_name='Artist')
    catalog_number = models.TextField(verbose_name='Catalog Number')
    title = models.TextField(verbose_name='Title')
    year = models.TextField(verbose_name='Year')
    image = models.TextField(verbose_name='Image')

    def __str__(self):
        return self.catalog_number

    class Meta:
        ordering = ('-year', )


class ReleasesDiscogs(models.Model):
    artist = models.TextField(verbose_name='Artist')
    catalog_number = models.TextField(verbose_name='Catalog Number')
    title = models.TextField(verbose_name='Title')
    year = models.TextField(verbose_name='Year')
    image = models.TextField(verbose_name='Image')

    def __str__(self):
        return self.catalog_number

    class Meta:
        ordering = ('-year', )
