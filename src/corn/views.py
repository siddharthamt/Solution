from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from corn.filters import CornFilter
from corn.models import Corn
from corn.serializers import CornSerializer


class CornListView(ListAPIView):
    queryset = Corn.objects.all()
    serializer_class = CornSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CornFilter
