import pytest
from faker import Faker

from apps.agro.models import Farmer, Culture, Farm


@pytest.fixture
def fake():
    fake = Faker('pt-br')
    return fake


@pytest.fixture
def farmer(db, fake):
    cpf = fake.cpf()
    name = fake.name()

    farmer = Farmer(name=name, document=cpf)
    farmer.save()
    return farmer


@pytest.fixture
def culture(db):
    return Culture.objects.create(name='Abobora fake')


@pytest.fixture
def farm(db, fake, farmer, culture):
    params = {
        'name': fake.company(),
        'owner_id': farmer.id,
        'total_area': 100,
        'vegetal_area': 20,
        'available_area': 80,
        'city': 'Ponta Porã',
        'state': 'MS'
    }
    farm = Farm.objects.create(**params)
    farm.cultures.add(culture)
    return farm
