import os
from django.core.management.base import BaseCommand
from datetime import datetime
import pandas as pd
from corn.models import Corn
from weather.models import Weather

WEATHER_DATA_TYPE = "weather"
CORN_YIELD_DATA_TYPE = "yield"

class Command(BaseCommand):
    def __init__(self):
        self.success_count = 0
        self.fail_count = 0
        super().__init__()
    
    help = "Data Ingestion"
    def add_arguments(self, parser):
        parser.add_argument(            
            "--weather",
            action="store_true",
            help="Ingest weather data from the wx_data folder",
        )
        parser.add_argument(            
            "--yield",
            action="store_true",
            help="Ingest yield data from the yld_data folder",
        )

    def handle(self, *args, **options):
        path = "../{}/"
        start_time = datetime.now()
        if options.get(WEATHER_DATA_TYPE, False):
            start_msg = f"Ingestion started for {WEATHER_DATA_TYPE} data at {start_time}."
            path = path.format("wx_data")
            self._read_txt_files(path, WEATHER_DATA_TYPE, start_msg)
        elif options.get(CORN_YIELD_DATA_TYPE, False):
            start_msg = f"Ingestion started for {CORN_YIELD_DATA_TYPE} data at at {start_time}."
            path = path.format("yld_data")
            self._read_txt_files(path, CORN_YIELD_DATA_TYPE, start_msg)
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to start data ingestion. Please specify --weather or --yield after 'ingest_data' in "
                    f"the command."
                )
            )
        return

    def _read_txt_files(self, path: str, data_type: str, start_msg: str) -> None:
        self.stdout.write(self.style.SUCCESS(start_msg))
        files = os.listdir(path)
        for file in files:
            if file.endswith(".txt"):
                file_name = file[:-4]
                file_path = path + file
                if data_type == WEATHER_DATA_TYPE:
                    self.ingest_weather_data(file_path, file_name)
                else:
                    self.ingest_yield_data(file_path)
                self.stdout.write(f"Ingestion completed for {file}")

        end_time = datetime.now()
        end_msg = f"Completed {data_type} data ingestion at {end_time}. No Of Records Ingested : {self.success_count}"
        self.stdout.write(self.style.SUCCESS(end_msg))

    def ingest_weather_data(self, file_path, file_name):        
        start_count = Weather.objects.all().count()
        df = pd.read_table(
            file_path,
            header=None,
            names=["date", "max_temp", "min_temp", "precipitation"],
        )
        df["station_id"] = file_name
        df["date"] = df["date"].apply(self._format_date)
        df["max_temp"] = df["max_temp"].apply(self._shift_decimal_by_one)
        df["min_temp"] = df["min_temp"].apply(self._shift_decimal_by_one)
        df["precipitation"] = df["precipitation"].apply(self._shift_decimal_by_two)
        records = df.to_dict("records")
        objs = [Weather(**record) for record in records]
        Weather.objects.bulk_create(objs, ignore_conflicts=True)
        curr_count = Weather.objects.all().count()
        self._update_counts(records, start_count, curr_count)

    def ingest_yield_data(self, file_path):        
        start_count = Corn.objects.all().count()
        df = pd.read_table(
            file_path,
            header=None,
            names=["year", "corn_yield"],
        )
        records = df.to_dict("records")
        objs = [Corn(**record) for record in records]
        returned_objs = Corn.objects.bulk_update_or_create(
            objs, ["corn_yield"], match_field="year", yield_objects=True
        )
        
        returned_objs = list(returned_objs)
        updated_objs = returned_objs[0][1]
        
        start_count -= len(updated_objs)
        curr_count = Corn.objects.all().count()
        self._update_counts(records, start_count, curr_count)

    def _format_date(self, date: str) -> str:

        date = str(date)
        year = date[:4]
        month = date[4:6]
        day = date[6:]
        formatted_date = f"{year}-{month}-{day}"
        return formatted_date

    def _shift_decimal_by_one(self, num: float) -> float:
        shifted_num = self._shift_decimal(num, -1)
        return round(shifted_num, 1)

    def _shift_decimal_by_two(self, num: float) -> float:
        shifted_num = self._shift_decimal(num, -2)
        return round(shifted_num, 2)

    def _shift_decimal(self, num: float, shift: int) -> float:        
        if num == -9999.0:
            return num
        shifted_num = num * 10.0**shift
        return shifted_num

    def _update_counts(self, records, start_count, curr_count):
        num_records = len(records)
        num_created = curr_count - start_count
        num_failed = num_records - num_created
        self.success_count += num_created
        self.fail_count += num_failed
