import re
from decimal import Decimal

from rest_framework import serializers
from rest_framework.validators import ValidationError
from validate_docbr import CPF, CNPJ

from apps.agro.models import Farm, Culture, Farmer, DOCUMENT_REGEX


class FarmerSerializer(serializers.ModelSerializer):
    cpfcnpj = serializers.CharField(write_only=True)

    class Meta:
        model = Farmer
        fields = ('id', 'name', 'document', 'cpfcnpj')
        read_only_fields = ('id', 'document')

    def validate_cpfcnpj(self, document):
        document = re.sub(DOCUMENT_REGEX, '', document)

        document_type = CNPJ()
        if len(document) == 11:
            document_type = CPF()

        if not document_type.validate(document):
            raise ValidationError('CPF/CNPJ is invalid')
        return document


class CultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culture
        fields = ('id', 'name')
        read_only_fields = ('id', 'name')


class FarmSerializer(serializers.ModelSerializer):
    cultures = CultureSerializer(read_only=True, many=True)
    owner = FarmerSerializer(read_only=False)
    culture_pks = serializers.PrimaryKeyRelatedField(write_only=True, many=True, queryset=Culture.objects.all())

    class Meta:
        model = Farm
        fields = ['id', 'name', 'owner', 'total_area', 'vegetal_area', 'available_area', 'city', 'state', 'cultures',
                  'culture_pks']
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data = self.format_validated_data(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = self.format_validated_data(validated_data)
        return super().update(instance, validated_data)

    def format_validated_data(self, validated_data):
        owner = validated_data.pop('owner')
        name = owner.get('name')

        document = owner.get('cpfcnpj')
        document = re.sub(DOCUMENT_REGEX, '', document)
        farmer, _ = Farmer.objects.get_or_create(document=document, defaults={'name': name})

        validated_data['owner_id'] = farmer.pk
        validated_data['cultures'] = validated_data.pop('culture_pks')
        return validated_data

    def validate_total_area(self, total_area):
        vegetal_area = Decimal(self.initial_data.get('vegetal_area'))
        available_area = Decimal(self.initial_data.get('available_area'))
        if total_area < vegetal_area + available_area:
            raise ValidationError('Invalid area, vegetal_area + available_area is greater than total_area')
        return total_area
