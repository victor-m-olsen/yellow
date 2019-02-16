import numpy as np
from scipy.stats import stats
from rasterUtils.rasterToArray import rasterToArray


def rasterStats(inRaster, cutline=None, cutlineAllTouch=True,
                referenceRaster=None, srcNoDataValue=None, quiet=False,
                bandToClip=1, statistics=['mean', 'median', 'std']):
    ''' Calculates the statistics of a raster layer. A refererence
    raster or a cutline geometry can be provided to narrow down the
    features for which the statistics are calculated.

    Args:
        inRaster (URL or GDAL.DataFrame): The raster to clip.

    **kwargs:
        cutline (URL or OGR.DataFrame): A geometry used to cut
        the inRaster.

        cutlineAllTouch (Bool): Should all pixels that touch
        the cutline be included? False is only pixel centroids
        that fall within the geometry.

        referenceRaster (URL or GDAL.DataFrame): A reference
        raster from where to clip the extent of the inRaster.

        cropToCutline (Bool): Should the output raster be
        clipped to the extent of the cutline geometry.

        srcNoDataValue (Number): Overwrite the nodata value of
        the source raster.

        quiet (Bool): Do not show the progressbars.

        bandToClip (Bool): Specify if only a specific band in
        the input raster should be clipped.

        statistics (List): A list containing all the statistics
        one would want to calculate. 'all' can be specified if
        every possible statistic is needed.

    Returns:
        Returns a dictionary with the requested statistics.
    '''

    # First: Turn the raster into a numpy array on which to calculate
    #        the statistics
    data = rasterToArray(
        inRaster,
        referenceRaster=referenceRaster,
        cutline=cutline,
        cutlineAllTouch=cutlineAllTouch,
        compressed=True,
        srcNoDataValue=srcNoDataValue,
        bandToClip=bandToClip,
        quiet=quiet,
        calcBandStats=False,
    )

    # If all types of statistics are requested insert all possible statistics
    # below. BEWARE: Slow..
    if statistics == 'all':
        statsToCalc = ['min', 'max', 'count', 'range', 'mean', 'median',
                       'std', 'kurtosis', 'skew', 'npskew', 'skewratio',
                       'variation', 'q1', 'q3', 'iqr', 'mad', 'madstd',
                       'with3std', 'within3st_mad']
    else:
        statsToCalc = statistics

    holder = {}

    for statType in statsToCalc:
        if statType == 'min':
            holder['min'] = np.min(data)

        elif statType == 'max':
            holder['max'] = np.max(data)

        elif statType == 'count':
            holder['count'] = len(data)

        elif statType == 'range':
            holder['min'] = np.min(data) if holder.get('min') is None else holder['min']
            holder['max'] = np.max(data) if holder.get('max') is None else holder['max']
            holder['range'] = holder['max'] - holder['min']

        elif statType == 'mean':
            holder['mean'] = np.mean(data)

        elif statType == 'median':
            holder['median'] = np.median(data)

        elif statType == 'std':
            holder['std'] = np.std(data)

        elif statType == 'kurtosis':
            holder['kurtosis'] = stats.kurtosis(data)

        elif statType == 'skew':
            holder['skew'] = stats.skew(data)

        elif statType == 'npskew':
            holder['mean'] = np.mean(data) if holder.get('mean') is None else holder['mean']
            holder['median'] = np.median(data) if holder.get('median') is None else holder['median']
            holder['std'] = np.std(data) if holder.get('std') is None else holder['std']

            holder['npskew'] = (holder['mean'] - holder['median']) / holder['std']

        elif statType == 'skewratio':
            holder['mean'] = np.mean(data) if holder.get('mean') is None else holder['mean']
            holder['median'] = np.median(data) if holder.get('median') is None else holder['median']

            holder['skewratio'] = holder['median'] / holder['mean']

        elif statType == 'variation':
            holder['variation'] = stats.variation(data)

        elif statType == 'q1':
            holder['q1'] = np.quantile(data, 0.25)

        elif statType == 'q3':
            holder['q3'] = np.quantile(data, 0.75)

        elif statType == 'iqr':
            holder['q1'] = np.quantile(data, 0.25) if holder.get('q1') is None else holder['q1']
            holder['q3'] = np.quantile(data, 0.75) if holder.get('q3') is None else holder['q3']

            holder['iqr'] = holder['q3'] - holder['q1']

        elif statType == 'mad':
            holder['median'] = np.median(data) if holder.get('median') is None else holder['median']

            deviations = np.abs(np.subtract(holder['median'], data))
            holder['mad'] = np.median(deviations)

        elif statType == 'madstd':
            holder['median'] = np.median(data) if holder.get('median') is None else holder['median']
            if holder.get('mad') is None:
                deviations = np.abs(np.subtract(holder['median'], data))
                holder['mad'] = np.median(deviations)

            holder['madstd'] = holder['mad'] * 1.4826

        elif statType == 'within3std':
            holder['count'] = len(data) if holder.get('count') is None else holder['count']
            holder['mean'] = np.mean(data) if holder.get('mean') is None else holder['mean']
            holder['std'] = np.std(data) if holder.get('std') is None else holder['std']

            _std3 = holder['std'] * 3
            lowerbound = holder['mean'] - _std3
            higherbound = holder['mean'] + _std3

            limit = holder['count'] - len(data[(data > lowerbound) & (data < higherbound)])

            holder['within3std'] = 100 - ((limit / holder['count']) * 100)

        elif statType == 'within3std_mad':
            holder['count'] = len(data) if holder.get('count') is None else holder['count']
            holder['median'] = np.median(data) if holder.get('median') is None else holder['median']
            if holder['mad'] == 0:
                deviations = np.abs(np.subtract(holder['median'], data))
                holder['mad'] = np.median(deviations)
                holder['madstd'] = holder['mad'] * 1.4826

            _std3 = holder['madstd'] * 3
            lowerbound = holder['median'] - _std3
            higherbound = holder['median'] + _std3

            limit = holder['count'] - len(data[(data > lowerbound) & (data < higherbound)])

            holder['within3std_mad'] = 100 - ((limit / holder['count']) * 100)

    return holder