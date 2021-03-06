import os

from tests.RME_test_case import RMETestCase
from weather_forecast_retrieval.grib2nc import grib2nc


class TestGrib2nc(RMETestCase):
    """Tests for `weather_forecast_retrieval` package."""

    def testGrib2nc(self):
        """
        Convert test data to netcdf
        """

        nc_file = self.output_path.joinpath(
            'hrrr.t04z.wrfsfcf01.nc'
        ).as_posix()
        grib_file = self.hrrr_dir.joinpath(
            'hrrr.20180722/hrrr.t04z.wrfsfcf01.grib2'
        ).as_posix()

        # get the data
        grib2nc(grib_file, nc_file, chunk_x=20, chunk_y=20)

        self.assertTrue(os.path.isfile(nc_file))
