import xarray as xr
import numpy as np

def cosweightlat(darray, lat1, lat2):
    """Calculate the weighted average for an [:,lat] array over the region
    lat1 to lat2
    """

    # flip latitudes if they are decreasing
    if (darray.lat[0] > darray.lat[darray.lat.size -1]):
        print("flipping latitudes")
        darray = darray.sortby('lat')

    region = darray.sel(lat=slice(lat1, lat2))
    weights=np.cos(np.deg2rad(region.lat))
    regionw = region.weighted(weights)
    regionm = regionw.mean("lat")

    return regionm
