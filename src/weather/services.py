from django.db.models import Max, Min, Avg, Sum

from weather.constants import MISSING_VALUE
from weather.models import Weather, Statistics


def generate_years_list() -> list:    
    if Weather.objects.all().count() == 0:
        return []
    min_date = Weather.objects.aggregate(Min("date"))
    max_date = Weather.objects.aggregate(Max("date"))
    start_year = min_date["date__min"].year
    end_year = max_date["date__max"].year
    total_years = end_year - start_year + 1
    years = list()
    for i in range(total_years):
        years.append(start_year + i)
    return years


def calculate_stats(years: list) -> None:    
    usable_max_data = Weather.objects.exclude(max_temp=MISSING_VALUE)
    usable_min_data = Weather.objects.exclude(min_temp=MISSING_VALUE)
    usable_precip_data = Weather.objects.exclude(precipitation=MISSING_VALUE)
    station_ids = set(Weather.objects.values_list("station_id", flat=True))
    for year in years:
        for station_id in station_ids:
            avg_max_temp = _calculate_avg_max_temp(usable_max_data, station_id, year)
            avg_min_temp = _calculate_avg_min_temp(usable_min_data, station_id, year)
            total_precipitation = _calculate_total_precip(
                usable_precip_data, station_id, year
            )
            defaults = {
                "avg_max_temp": avg_max_temp,
                "avg_min_temp": avg_min_temp,
                "total_precipitation": total_precipitation,
            }
            Statistics.objects.update_or_create(
                station_id=station_id, year=year, defaults=defaults
            )


def _calculate_avg_max_temp(usable_max_data, station_id, year):
    try:
        filtered_data = usable_max_data.filter(station_id=station_id, date__year=year)
        aggregate = filtered_data.aggregate(Avg("max_temp"))
        avg_max_temp = aggregate["max_temp__avg"]
        rounded_avg_max_temp = round(avg_max_temp, 2)
        return rounded_avg_max_temp
    except Exception:
        return None


def _calculate_avg_min_temp(usable_min_data, station_id, year):
    try:
        filtered_data = usable_min_data.filter(station_id=station_id, date__year=year)
        aggregate = filtered_data.aggregate(Avg("min_temp"))
        avg_min_temp = aggregate["min_temp__avg"]
        rounded_avg_min_temp = round(avg_min_temp, 2)
        return rounded_avg_min_temp
    except Exception:
        return None


def _calculate_total_precip(usable_precip_data, station_id, year):
    try:
        filtered_data = usable_precip_data.filter(
            station_id=station_id, date__year=year
        )
        aggregate = filtered_data.aggregate(Sum("precipitation"))
        total_precipitation = aggregate["precipitation__sum"]
        rounded_total_precipitation = round(total_precipitation, 2)
        return rounded_total_precipitation
    except Exception:
        return None
