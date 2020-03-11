import sys; sys.path.append('..')
import numpy as np
from time import time
from lib.raster_io import raster_to_array, array_to_raster
from lib.stats_filters import standardise_filter

folder = '/mnt/c/users/caspe/desktop/data/'
in_path = folder + 'B04.jp2'
in_raster = raster_to_array(in_path).astype(np.double)

array_to_raster(standardise_filter(in_raster), out_raster=folder + 'b4_standard.tif', reference_raster=in_path)
array_to_raster(standardise_filter(in_raster, True), out_raster=folder + 'b4_standard_scaled.tif', reference_raster=in_path)