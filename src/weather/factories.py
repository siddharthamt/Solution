from datetime import date
from factory import Sequence
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText, FuzzyFloat, FuzzyDate, FuzzyInteger

from weather.models import Weather, Statistics


class WeatherFactory(DjangoModelFactory):
    class Meta:
        model = Weather

    station_id = Sequence(lambda n: n)
    date = FuzzyDate(date.fromisoformat("1950-01-01"))
    max_temp = FuzzyFloat(low=16, high=32)
    min_temp = FuzzyFloat(low=0, high=16)
    precipitation = FuzzyFloat(low=0, high=12)


class StatisticsFactory(DjangoModelFactory):
    class Meta:
        model = Statistics

    station_id = Sequence(lambda n: n)
    year = FuzzyInteger(low=1900, high=2200)
    avg_max_temp = FuzzyFloat(low=0)
    avg_min_temp = FuzzyFloat(low=0)
    total_precipitation = FuzzyFloat(low=0)
