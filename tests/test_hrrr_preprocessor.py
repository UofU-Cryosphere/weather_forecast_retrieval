import pandas as pd

from tests.RME_test_case import RMETestCase
from weather_forecast_retrieval.hrrr import HRRR
from weather_forecast_retrieval.hrrr_preprocessor import HRRRPreprocessor


class TestHRRRPreprocessor(RMETestCase):
    """
    Test cropping HRRR files

    The test HRRR files in this repo don't have TCDC variable in their GRIB
    file.
    """

    start_date = '2018-07-22 01:00'
    end_date = '2018-07-22 02:00'
    output_files = [
            'hrrr.20180722/hrrr.t01z.wrfsfcf01.grib2',
            'hrrr.20180722/hrrr.t02z.wrfsfcf01.grib2',
        ]

    def setUp(self):
        super().setUp()
        self.test_subject = HRRRPreprocessor(
            self.hrrr_dir.as_posix(),
            self.start_date,
            self.end_date,
            self.output_path.as_posix(),
            [-116.9, 42.9, -116.5, 43.2],
            1,
            verbose=True
        )

    def test_bad_file(self):
        self.test_subject.run()

        for file in self.output_files:
            self.assertFalse(
                self.output_path.joinpath(file).exists(),
                'File {} was written although no TCDC variable '
                'in GRIB source file'.format(file)
            )

    def test_pre_process(self):
        self.test_subject.variables.pop(-1)
        self.test_subject.run()

        for file in self.output_files:
            self.assertTrue(
                self.output_path.joinpath(file).exists(),
                'File {} was not written successfully'.format(file)
            )

        metadata, data = HRRR().get_saved_data(
            pd.to_datetime(self.end_date),
            pd.to_datetime('2018-07-22 03:00'),
            self.BBOX,
            file_type='grib2',
            output_dir=self.output_path.as_posix(),
            force_zone_number=self.UTM_ZONE_NUMBER)

        self.assertListEqual(
            list(data.keys()),
            ['air_temp', 'relative_humidity', 'wind_u', 'wind_v', 'precip_int', 'short_wave']
        )
