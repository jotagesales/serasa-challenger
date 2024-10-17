import pytest
from faker import Faker

from apps.agro.models import Farmer, Culture


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
