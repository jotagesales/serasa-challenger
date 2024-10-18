from django.db.models import Count, Sum, F
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.agro.models import Farm
from .serializers import FarmSerializer


class FarmViewSet(viewsets.ModelViewSet):
    serializer_class = FarmSerializer
    queryset = Farm.objects.select_related('owner').prefetch_related('cultures').all()
    permission_classes = [AllowAny]


class FarmAnalyticsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Farm.objects.all()

        usage = queryset.values('id', 'name').annotate(
            usage=Sum(
                F('vegetal_area') + F('available_area')
            )
        )

        farms_by_state = queryset.values('state').annotate(count_farms=Count('id'))
        farms_by_culture = queryset.values('cultures__id', 'cultures__name').annotate(count_farms=Count('id'))

        totals = queryset.aggregate(count_farms=Count('id'), total_area=Sum('total_area'))

        totals.update({
            'farms': farms_by_state.all(),
            'cultures': farms_by_culture.all(),
            'usage': usage.all()
        })
        return Response(totals)
