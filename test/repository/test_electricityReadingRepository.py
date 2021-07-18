import dataclasses
from unittest import TestCase

from domain.electricity_reading import ElectricityReading
from repository.electricity_reading_repository import ElectricityReadingRepository


class TestElectricityReadingRepository(TestCase):
    def setUp(self):
        self.electricity_reading_repository = ElectricityReadingRepository()
        self.electricity_reading_repository.store('smart-meter-0', [
            ElectricityReading({'time': 1507375234, 'reading': 0.5}),
            ElectricityReading({'time': 1510053634, 'reading': 0.75}),
            ElectricityReading({'time': 1527375234, 'reading': 0.876}),
            ElectricityReading({'time': 1530053634, 'reading': 0.3}),
        ])

    def test_have_new_entry_when_new_smart_meter_id_is_given(self):
        readings = self.electricity_reading_repository.find('smart-meter-0')
        self.assertDictEqual({'time': 1507375234, 'reading': 0.5}, dataclasses.asdict(readings[0]))
        self.assertDictEqual({'time': 1510053634, 'reading': 0.75}, dataclasses.asdict(readings[1]))

    def test_add_usage_data_against_smart_meter_id_if_it_already_exists(self):
        previous_readings = self.electricity_reading_repository.find('smart-meter-0')
        
        self.electricity_reading_repository \
            .store(
                'smart-meter-0',
                [ElectricityReading({'time': 1510572000, 'reading': 0.32})])
        
        # Compares new size to previous
        readings = self.electricity_reading_repository.find('smart-meter-0')
        self.assertEqual(len(previous_readings) + 1, len(readings))

        # Ensures that previous elements are still stored with no change
        self.assertTrue(
            all(
                [previous_reading in readings for previous_reading in previous_readings]
            ))
        
        # Asserts that the additional new element was stored
        self.assertIn(ElectricityReading({'time': 1510572000, 'reading': 0.32}), readings)
 