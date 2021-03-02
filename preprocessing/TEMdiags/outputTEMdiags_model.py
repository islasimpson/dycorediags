# Script to calculate TEM diagnostics
# This assumes the data have already been organized into zonal mean fluxes
# Uzm, THzm, VTHzm, Vzm, UVzm, UWzm, Wzm as was done by ctem.F90 for FV dycore
# note that here we are calculating the E-P fluxes on model levels, which is ok
# in the stratosphere but not in the troposphere.  If interested in tropospheric
# E-P flux diagnostics, make sure they have been interpolated to pressure already.

# Isla Simpson Feb 25th 2021

import xarray as xr
import numpy as np
from scipy import integrate

# set experiment names to process
expname=[ "L70_bugfix" ]
#expname=[ "sponge5", "defaultsponge", "sponge5-marshian" ]

# set basepath which contains the flux data
basepath="/project/cas/islas/verticalresolution/TEMdiags/"

# set output directory
outdir="/project/cas/islas/python_savs/dycorediags/preprocessing/TEMdiags/"

# set up constants for TEM calculations
p0=101325. 
a=6.371e6
om=7.29212e-5
H=7000.
g0=9.80665


for iexp in expname:

    fpath=basepath+iexp+"/TEMdiags*.nc"
    #fpath=basepath+"TEMdiags*.nc"
    print(fpath)
    dat = xr.open_mfdataset(fpath, coords="minimal", join="override", decode_times=True)
    dat = dat.squeeze()

    latrad = np.array((dat.lat/180.)*np.pi)
    f=2.*om*np.sin(latrad[:])

    uzm = np.array(dat.Uzm)
    thzm = np.array(dat.THzm)
    vthzm = np.array(dat.VTHzm)
    vzm = np.array(dat.Vzm)
    uvzm = np.array(dat.UVzm)
    uwzm = np.array(dat.UWzm)
    wzm = np.array(dat.Wzm)
    #pre = np.array(dat.pre)
    pre = np.array(dat.ilev)
    lat = np.array(dat.lat)

    npre = pre.size
    nlat = lat.size
    ntime = dat.time.size

    # setup pre(ntime,npre,nlat) and latrad(ntime,npre,nlat)
    latradarray = np.tile(latrad,npre*ntime)
    latradarray = np.reshape(latradarray,[ntime,npre,nlat])

    prearray = np.tile(pre,nlat*ntime)
    prearray = np.reshape(prearray,[ntime,nlat,npre])
    prearray = np.moveaxis(prearray,2,1)

    # convert w terms from m/s to Pa/s
    uwzm = -1.*uwzm*prearray*100./H
    wzm = -1.*wzm*prearray*100./H

    # compute the latitudinal gradient of U
    dudphi = (1./a)*np.gradient(uzm*np.cos(latradarray), latrad, axis=2)

    # compute the vertical gradient of theta and u
    dthdp = np.gradient(thzm, pre*100.,axis=1)
    dudp = np.gradient(uzm, pre*100., axis=1)

    # compute eddy streamfunction and its vertical gradient
    psieddy = vthzm/dthdp
    dpsidp = np.gradient(psieddy,pre*100.,axis=1)

    # (1/acos(phii))**d(psi*cosphi/dphi) for getting w*
    psicos = psieddy*np.cos(latradarray)
    dpsidy = (1./(a*np.cos(latradarray)))*np.gradient(psicos,latrad,axis=2)

    # TEM vertical velocity (Eq A7 of dynvarmip)
    wtem = wzm+dpsidy

    # utendwtem (Eq A10 of dynvarmip)
    utendwtem = -1.*wtem*dudp

    # vtem (Eq A6 of dynvarmip)
    vtem = vzm-dpsidp
    
    # utendvtem (Eq A9 of dynvarmip)
    farray = np.tile(f,npre*ntime)
    farray = np.reshape(farray,[ntime,npre,nlat])
    utendvtem = vtem*(farray - dudphi) 
    
    # calculate E-P fluxes
    epfy = a*np.cos(latradarray)*(dudp*psieddy - uvzm) # A2
    epfz = a*np.cos(latradarray)*( (farray-dudphi)*psieddy - uwzm) # A3
    
    # calculate E-P flux divergence and zonal wind tendency due to resolved waves (A5)
    depfydphi = np.gradient(epfy*np.cos(latradarray),latrad, axis=2)*(1./(a*np.cos(latradarray)))
    depfzdp = np.gradient(epfz,pre*100.,axis=1)
    utendepfd = depfydphi + depfzdp
    utendepfd = (1./(a*np.cos(latradarray)))*utendepfd

    # TEM stream function, Eq (A8)
    topvzm = np.zeros([ntime,1,nlat])
    vzmwithzero = np.concatenate((topvzm, vzm), axis=1)
    toppre = np.zeros([1])
    prewithzero = np.concatenate((toppre, pre))
    intv = integrate.cumtrapz(vzmwithzero,prewithzero*100.,axis=1)
    psitem = (2*np.pi*a*np.cos(latradarray)/g0)*(intv - psieddy)

    # final scaling of E-P fluxes and divergence to transform to log-pressure
    epfy = epfy*(prearray*100.)/p0 # A13
    epfz = -1.*(H/p0)*epfz # A14
    wtem = -1.*(H/(prearray*100.))*wtem # A16

    uzm = xr.DataArray(uzm, coords = dat.Uzm.coords, name='uzm', 
                     attrs={'long_name':'zonal mean zonal wind', 'units':'m/s'})
    epfy = xr.DataArray(epfy, coords = dat.Uzm.coords, name='epfy', 
                     attrs={'long_name':'northward component of E-P flux', 'units':'m3/s2'})
    epfz = xr.DataArray(epfz, coords = dat.Uzm.coords, name='epfz', 
                     attrs={'long_name':'upward component of E-P flux', 'units':'m2/s2'})
    vtem = xr.DataArray(vtem, coords = dat.Uzm.coords, name='vtem', 
                     attrs={'long_name':'Transformed Eulerian mean northward wind', 'units':'m/s'})
    wtem = xr.DataArray(wtem, coords = dat.Uzm.coords, name='wtem', 
                     attrs={'long_name':'Transformed Eulerian mean upward wind','units':',/s'})
    psitem = xr.DataArray(psitem, coords = dat.Uzm.coords, name='psitem',
                     attrs={'long_name':'Transformed Eulerian mean mass stream function','units':'kg/s'})
    utendepfd = xr.DataArray(utendepfd, coords = dat.Uzm.coords, name='utendepfd',
                     attrs={'long_name':'tendency of eastward wind due to Eliassen-Palm flux divergence',
                           'units':'m/s2'})
    utendvtem = xr.DataArray(utendvtem, coords = dat.Uzm.coords, name='utendvtem',
    attrs={'long_name':'tendency of eastward wind due to TEM northward wind advection and the coriolis term'
              ,'units':'m/s2'})
    utendwtem = xr.DataArray(utendwtem, coords = dat.Uzm.coords, name='utendwtem',
    attrs={'long_name':'tendency of eastward wind due to TEM upward wind advection','units':'m/s2'})

#    uzm = uzm.rename({"ilev":"pre"})
#    epfy = epfy.rename({"ilev":"pre"})
#    epfz = epfz.rename({"ilev":"pre"})
#    vtem = vtem.rename({"ilev":"pre"})
#    wtem = wtem.rename({"ilev":"pre"})
#    psitem = psitem.rename({"ilev":"pre"})
#    utendepfd = utendepfd.rename({"ilev":"pre"})
#    utendvtem = utendvtem.rename({"ilev":"pre"})
#    utendwtem = utendwtem.rename({"ilev":"pre"})    

    uzm.to_netcdf(outdir+iexp+".nc")
    epfy.to_netcdf(outdir+iexp+".nc", mode="a")
    epfz.to_netcdf(outdir+iexp+".nc", mode="a")
    vtem.to_netcdf(outdir+iexp+".nc", mode="a")
    wtem.to_netcdf(outdir+iexp+".nc", mode="a")
    psitem.to_netcdf(outdir+iexp+".nc", mode="a")
    utendepfd.to_netcdf(outdir+iexp+".nc", mode="a")
    utendvtem.to_netcdf(outdir+iexp+".nc", mode="a")
    utendwtem.to_netcdf(outdir+iexp+".nc", mode="a")




