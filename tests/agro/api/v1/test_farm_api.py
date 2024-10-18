import json
import re

import pytest
from django.urls import reverse

from apps.agro.models import Farmer, Farm, DOCUMENT_REGEX


def test_pagination_default_fields(db, client):
    url = reverse('farm-list')
    response = client.get(url)

    data = response.json()

    assert response.status_code == 200
    assert 'count' in data.keys()
    assert 'next' in data.keys()
    assert 'previous' in data.keys()
    assert 'results' in data.keys()


def test_list_farm(client, farm):
    url = reverse('farm-list')
    response = client.get(url)

    data = response.json()['results']

    expected = [
        {
            'id': farm.id,
            'name': farm.name,
            'owner': {
                'id': farm.owner.id,
                'name': farm.owner.name,
                'document': farm.owner.document
            },
            'total_area': '100.00',
            'vegetal_area': '20.00',
            'available_area': '80.00',
            'city': farm.city,
            'state': farm.state,
            'cultures': [
                {
                    'id': farm.cultures.first().id,
                    'name': farm.cultures.first().name
                }
            ]
        }
    ]

    assert response.status_code == 200
    assert data == expected


@pytest.mark.parametrize('document', ['123.456.789-09', '93.225.797/0001-06'])
def test_farm_create(document, client, fake, culture):
    url = reverse('farm-list')

    name = fake.company()
    city = fake.city()
    state = fake.state_abbr()

    payload = {
        "name": name,
        "owner": {
            "cpfcnpj": document,
            "name": fake.name()
        },
        "total_area": "100",
        "vegetal_area": "10",
        "available_area": "10",
        "city": city,
        "state": state,
        "culture_pks": [culture.pk]
    }
    response = client.post(url, data=json.dumps(payload), content_type='application/json')
    data = response.json()

    farm_id = data.get('id')

    farm = Farm.objects.get(pk=farm_id)

    assert response.status_code == 201
    assert farm.owner.document == re.sub(DOCUMENT_REGEX, '', document)


def test_farm_create_validation_total_area(client, fake, culture):
    url = reverse('farm-list')

    name = fake.company()
    city = fake.city()
    state = fake.state_abbr()

    payload = {
        "name": name,
        "owner": {
            "cpfcnpj": fake.cnpj(),
            "name": fake.name()
        },
        "total_area": "100",
        "vegetal_area": "110",
        "available_area": "10",
        "city": city,
        "state": state,
        "culture_pks": [culture.pk]
    }
    response = client.post(url, data=json.dumps(payload), content_type='application/json')
    expected = {'total_area': ['Invalid area, vegetal_area + available_area is greater than total_area']}

    assert response.status_code == 400
    assert response.json() == expected


def test_owner_has_too_many_farms(client, fake, farm, culture):
    url = reverse('farm-list')

    name = fake.company()
    city = fake.city()
    state = fake.state_abbr()

    payload = {
        "name": name,
        "owner": {
            "cpfcnpj": farm.owner.document,
            "name": farm.owner.name
        },
        "total_area": "100",
        "vegetal_area": "10",
        "available_area": "10",
        "city": city,
        "state": state,
        "culture_pks": [culture.pk]
    }
    response = client.post(url, data=json.dumps(payload), content_type='application/json')

    farmer = Farmer.objects.get(document=farm.owner.document)

    assert response.status_code == 201
    assert farmer.farm.count() == 2


def test_farm_detail(client, farm):
    url = reverse('farm-detail', kwargs={'pk': farm.id})
    response = client.get(url)

    data = response.json()

    expected = {
        'id': farm.id,
        'name': farm.name,
        'owner': {
            'id': farm.owner.id,
            'name': farm.owner.name,
            'document': farm.owner.document
        },
        'total_area': '100.00',
        'vegetal_area': '20.00',
        'available_area': '80.00',
        'city': farm.city,
        'state': farm.state,
        'cultures': [
            {
                'id': farm.cultures.first().id,
                'name': farm.cultures.first().name
            }
        ]
    }

    assert response.status_code == 200
    assert data == expected


def test_farm_delete(client, farm):
    url = reverse('farm-detail', kwargs={'pk': farm.id})
    response = client.delete(url)

    assert response.status_code == 204
    with pytest.raises(Farm.DoesNotExist):
        Farm.objects.get(id=farm.id)


def test_farm_analytics(client, farm):
    url = reverse('farm-analytics')
    response = client.get(url)
    data = response.json()

    expected = {
        "count_farms": 1,
        "total_area": farm.total_area,
        "farms": [
            {
                "state": farm.state,
                "count_farms": 1
            },
        ],
        "cultures": [
            {
                "cultures__id": farm.cultures.first().id,
                "cultures__name": farm.cultures.first().name,
                "count_farms": 1
            },
        ],
        "usage": [
            {
                "id": farm.id,
                "name": farm.name,
                "usage": farm.vegetal_area + farm.available_area
            }
        ]
    }
    assert response.status_code == 200
    assert data == expected
