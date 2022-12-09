from rest_framework import serializers

from weather.models import Weather, Statistics


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = [
            "station_id",
            "date",
            "max_temp",
            "min_temp",
            "precipitation",
            "created_at",
            "updated_at",
        ]


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = [
            "station_id",
            "year",
            "avg_max_temp",
            "avg_min_temp",
            "total_precipitation",
            "created_at",
            "updated_at",
        ]
