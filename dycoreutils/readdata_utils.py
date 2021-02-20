# routines for reading in data in various forms

import xarray as xr
import pandas as pd
import numpy as np

def read_cesm_zonalmean(filepath, datestart, dateend):
    """Read in a time slice and calculate the zonal mean.
    Accounts for CESM's wierd calendar.  Setting the time axis as the 
    average of time_bnds.
    Args:
        filepath (string) = location of files
        datestart (string) = start date for timeslice (in a normal calendar)
        dateend (string) = enddate for timeslice (in a normal calendar)
    """

    dat = xr.open_mfdataset(filepath, coords="minimal", join="override", decode_times = True).mean("lon")

    try:
        try:
            timebndavg = np.array(dat.time_bnds,
                     dtype='datetime64[s]').view('i8').mean(axis=1).astype('datetime64[s]')
        except:
            timebndavg = np.array(dat.time_bounds,
                     dtype='datetime64[s]').view('i8').mean(axis=1).astype('datetime64[s]')


        dat['time'] = timebndavg
    except:
        print("warning, you're reading CESM data but there's no time_bnds")
        print("make sure you're reading in what you're expecting to")

    dat = dat.sel(time=slice(datestart, dateend))

    return dat

