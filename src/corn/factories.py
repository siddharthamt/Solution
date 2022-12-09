from factory import Sequence
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from corn.models import Corn


class CornFactory(DjangoModelFactory):
    class Meta:
        model = Corn

    year = Sequence(lambda n: 1950 + n)
    corn_yield = FuzzyInteger(low=0)
