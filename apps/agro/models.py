import re

from django.db import models

DOCUMENT_REGEX = r'(\.|\-|\/)'


class Farmer(models.Model):
    name = models.CharField('Nome', max_length=150)
    document = models.CharField('CPF/CNPJ', max_length=14, unique=True)

    class Meta:
        db_table = 'farmer'

    def save(self, *args, **kwargs):
        self.document = re.sub(DOCUMENT_REGEX, '', self.document)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.document} - {self.name}'


class Culture(models.Model):
    name = models.CharField('Cultura', max_length=150)

    class Meta:
        db_table = 'culture'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Farm(models.Model):
    name = models.CharField('Nome', max_length=150)
    owner = models.ForeignKey('Farmer', related_name='farm', on_delete=models.DO_NOTHING)
    total_area = models.DecimalField('Area total', max_digits=11, decimal_places=2)
    vegetal_area = models.DecimalField('Area Vegetação', max_digits=11, decimal_places=2)
    available_area = models.DecimalField('Area agricutável', max_digits=11, decimal_places=2)

    # normaly i would use the IBGE tables to list cities
    # but for this test i've prefered using this way
    city = models.CharField('Cidade', max_length=100)
    state = models.CharField('Estado', max_length=2)

    cultures = models.ManyToManyField('Culture', related_name='farms')

    class Meta:
        db_table = 'farm'

    def __str__(self):
        return self.name
