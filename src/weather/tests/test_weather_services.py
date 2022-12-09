import pytest
from datetime import date

from weather.constants import MISSING_VALUE

from weather.factories import WeatherFactory, StatisticsFactory
from weather.models import Statistics
from weather.services import generate_years_list, calculate_stats


@pytest.mark.django_db
class TestWeatherServices:
    @pytest.mark.parametrize(
        "start_year, end_year", ((1985, 1985), (1985, 1986), (1985, 2014))
    )
    def test_generate_years_list(self, start_year, end_year):
        start_date = f"{start_year}-01-01"
        end_date = f"{end_year}-12-31"
        WeatherFactory.create(date=date.fromisoformat(start_date))
        WeatherFactory.create(date=date.fromisoformat(end_date))
        expected_num_years = end_year - start_year + 1

        returned_years = generate_years_list()

        assert len(returned_years) == expected_num_years
        assert returned_years[0] == start_year
        assert returned_years[expected_num_years - 1] == end_year
        for i in range(expected_num_years - 1):
            assert returned_years[i] + 1 == returned_years[i + 1]

    def test_generate_years_list_no_data(self):
        returned_years = generate_years_list()
        assert not returned_years

    def test_calculate_stats(self):
        batch_size = 5
        year_1 = 1999
        year_2 = 2000
        years = [year_1, year_2]
        date_1 = f"{year_1}-02-25"
        date_2 = f"{year_2}-10-10"
        station_id_1 = "USC12345"
        station_id_2 = "USC67890"
        station_ids = [station_id_1, station_id_2]

        dataset_1 = list()
        dataset_2 = list()
        dataset_3 = list()
        dataset_4 = list()
        datasets = [dataset_1, dataset_2, dataset_3, dataset_4]
        set_num = 0
        for year in years:
            for station_id in station_ids:
                for i in range(1, batch_size + 1):
                    date_str = f"{year}-01-0{i}"
                    print(date_str)
                    data = WeatherFactory.create(
                        station_id=station_id, date=date.fromisoformat(date_str)
                    )
                    datasets[set_num].append(data)
                set_num += 1

        WeatherFactory.create(
            station_id=station_id_1,
            date=date.fromisoformat(date_1),
            max_temp=MISSING_VALUE,
            min_temp=MISSING_VALUE,
            precipitation=MISSING_VALUE,
        )
        WeatherFactory.create(
            station_id=station_id_1,
            date=date.fromisoformat(date_2),
            max_temp=MISSING_VALUE,
            min_temp=MISSING_VALUE,
            precipitation=MISSING_VALUE,
        )

        calculate_stats(years)

        for dataset in datasets:
            record = dataset[0]
            year = record.date.year
            station_id = record.station_id
            (
                avg_max_temp,
                avg_min_temp,
                total_precipitation,
            ) = self._calculate_expected_stats(dataset, batch_size)
            statistics = Statistics.objects.get(station_id=station_id, year=year)
            assert avg_max_temp == statistics.avg_max_temp
            assert avg_min_temp == statistics.avg_min_temp
            assert total_precipitation == statistics.total_precipitation

    def test_calculate_stats_upsert(self):
        year = 1999
        years = [
            year,
        ]
        iso_date = f"{year}-02-25"
        station_id = "USC12345"
        max_temp = 20.1
        min_temp = 12.9
        precipitation = 0.76

        WeatherFactory.create(
            station_id=station_id,
            date=date.fromisoformat(iso_date),
            max_temp=max_temp,
            min_temp=min_temp,
            precipitation=precipitation,
        )
        StatisticsFactory.create(
            station_id=station_id,
            year=year,
            avg_max_temp=0,
            avg_min_temp=0,
            total_precipitation=0,
        )

        calculate_stats(years)

        statistics = Statistics.objects.get(station_id=station_id, year=year)
        assert statistics.avg_max_temp == max_temp
        assert statistics.avg_min_temp == min_temp
        assert statistics.total_precipitation == precipitation

    def test_calculate_stats_no_data(self):
        year = 1999
        bad_year = 2000
        years = [year, bad_year]
        iso_date = f"{year}-02-25"
        station_id = "USC12345"
        WeatherFactory.create(
            station_id=station_id, date=date.fromisoformat(iso_date)
        )

        calculate_stats(years)

        null_stat = Statistics.objects.get(station_id=station_id, year=bad_year)
        assert not null_stat.avg_max_temp
        assert not null_stat.avg_min_temp
        assert not null_stat.total_precipitation

    def _calculate_expected_stats(self, dataset, batch_size):
        total_max_temp = 0
        total_min_temp = 0
        total_precipitation = 0

        for record in dataset:
            total_max_temp += record.max_temp
            total_min_temp += record.min_temp
            total_precipitation += record.precipitation

        avg_max_temp = total_max_temp / batch_size
        avg_min_temp = total_min_temp / batch_size
        rounded_avg_max_temp = round(avg_max_temp, 2)
        rounded_avg_min_temp = round(avg_min_temp, 2)
        rounded_total_precipitation = round(total_precipitation, 2)

        return rounded_avg_max_temp, rounded_avg_min_temp, rounded_total_precipitation
