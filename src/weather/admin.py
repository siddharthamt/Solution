from django.contrib.admin import register, ModelAdmin

from weather.models import Weather, Statistics
from weather.services import generate_years_list, calculate_stats


@register(Weather)
class WeatherAdmin(ModelAdmin):
    list_display = [
        "station_id",
        "date",
        "max_temp",
        "min_temp",
        "precipitation",
    ]
    list_filter = ["station_id", "date"]
    ordering = ["station_id", "date"]  # todo: apply ordering to apis
    actions = [
        "calculate_all_statistics",
    ]

    def calculate_all_statistics(self, request, queryset):
        years = generate_years_list()
        if years:
            calculate_stats(years)
        return

    calculate_all_statistics.short_description = "Calculate All Statistics"


@register(Statistics)
class StatisticsAdmin(ModelAdmin):
    list_display = [
        "station_id",
        "year",
        "avg_max_temp",
        "avg_min_temp",
        "total_precipitation",
    ]
    list_filter = ["station_id", "year"]
    ordering = ["station_id", "year"]
