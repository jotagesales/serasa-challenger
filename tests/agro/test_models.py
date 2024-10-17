import re

import pytest
from django.db.utils import DataError

from apps.agro.models import Farmer, DOCUMENT_REGEX, Farm, Culture


def test_create_farmer_cpf(db, fake):
    cpf = fake.cpf()
    name = fake.name()

    farmer = Farmer(name=name, document=cpf)
    farmer.save()

    assert farmer.id
    assert farmer.document == re.sub(DOCUMENT_REGEX, '', cpf)
    assert str(farmer) == f'{farmer.document} - {farmer.name}'


def test_create_farmer_cnpj(db, fake):
    cnpj = fake.cnpj()
    name = fake.name()

    farmer = Farmer(name=name, document=cnpj)
    farmer.save()

    assert farmer.id
    assert farmer.document == re.sub(DOCUMENT_REGEX, '', cnpj)


def test_create_farmer_long_document(db, fake):
    invalid_document = '123456789123456'
    name = fake.name()

    with pytest.raises(DataError):
        farmer = Farmer(name=name, document=invalid_document)
        farmer.save()


def test_create_farm(farmer, fake):
    params = {
        'name': fake.company(),
        'owner': farmer,
        'total_area': 100.75,
        'vegetal_area': 30.56,
        'available_area': 70.19,
        'city': 'Ponta Porã',
        'state': 'MS'
    }
    farm = Farm(**params)
    farm.save()

    for culture in Culture.objects.all():
        farm.cultures.add(culture)

    assert farm
    assert farm.cultures.count() == Culture.objects.count()
    assert str(farm) == farm.name


def test_create_farm_invalid_state(farmer, fake):
    params = {
        'name': fake.company(),
        'owner': farmer,
        'total_area': 100.75,
        'vegetal_area': 30.56,
        'available_area': 70.19,
        'city': 'Ponta Porã',
        'state': 'MSS'
    }
    with pytest.raises(DataError):
        Farm.objects.create(**params)


def test_repr_culture(culture):
    assert str(culture) == culture.name
