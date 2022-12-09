from django_filters import FilterSet, CharFilter

from corn.models import Corn


class CornFilter(FilterSet):
    year = CharFilter(field_name="year", lookup_expr="iexact")

    class Meta:
        model = Corn
        fields = ["year"]
