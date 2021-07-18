from flask import abort

from repository.electricity_reading_repository import ElectricityReadingRepository
from service.electricity_reading_service import ElectricityReadingService

repository = ElectricityReadingRepository()
service = ElectricityReadingService(repository)


def store(data):
    service.store_reading(data)
    return data


def read(smart_meter_id):
    readings = service.retrieve_readings_for(smart_meter_id)
    if len(readings) < 1:
        abort(404)
    else:
        return [r.to_json() for r in readings]

def read_week(smart_meter_id: str, date: int) -> []:
    max_interval = date

    readings = service.retrieve_readings_for_week(smart_meter_id, date)
    if len(readings) < 1:
        abort(404)
    else:
        return [r.to_json() for r in readings]
