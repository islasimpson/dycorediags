import matplotlib.pyplot as plt
import numpy as np
from dycoreutils import colormap_utils as mycolors
import sys

def get3by3coords():
    """ positioning for 3x3 plots """
    x1 = [0.04,0.37,0.7,0.04,0.37,0.7,0.04,0.37,0.7]
    x2 = [0.31,0.64,0.97,0.31,0.64,0.97,0.31,0.64,0.97]
    y1 = [0.8,0.8,0.8,0.59,0.59,0.59,0.38,0.38,0.38]
    y2 = [0.95,0.95,0.95,0.74,0.74,0.74,0.53,0.53,0.53]

    return x1, x2, y1, y2

def get4by4coords():
    """ positioning for 4x4 plots """
    x1 = [0.04,0.28,0.52,0.76,0.04,0.28,0.52,0.76,0.04,0.28,0.52,0.76,0.04,0.28,0.52,0.76]
    x2 = [0.22,0.46,0.7,0.94,0.22,0.46,0.7,0.94,0.22,0.46,0.7,0.94,0.22,0.46,0.7,0.94]
    y1 = [0.8,0.8,0.8,0.8,0.59,0.59,0.59,0.59,0.38,0.38,0.38,0.38,0.17,0.17,0.17,0.17]
    y2 = [0.95,0.95,0.95,0.95,0.74,0.74,0.74,0.74,0.53,0.53,0.53,0.53,0.32,0.32,0.32,0.32]
 
    return x1, x2, y1, y2

   
def plotlatlogpre_to0p01(fig, data, lat, pre, ci, cmin, cmax, titlestr, x1=0.1, x2=0.9, y1=0.1, y2=0.9):
    """
    Plot a pressure versus latitude contour plot up to 0.01hPa.
    """

    # set up contour levels and color map
    nlevs = (cmax-cmin)/ci + 1
    clevs = np.arange(cmin, cmax+ci, ci)
    mymap = mycolors.blue2red_cmap(nlevs)

    plt.rcParams['font.size'] = '12'
    
    ax = fig.add_axes([x1, y1, x2-x1, y2-y1])

    ax.contourf(lat,-1.*np.log10(pre), data, levels=clevs, cmap=mymap, extend='max')
    ax.contour(lat,-1.*np.log10(pre), data, levels=clevs, colors='black', linewidths=0.5)
    ax.set_ylim(-np.log10(1000.),-np.log10(0.01))
    ax.set_yticks([-np.log10(1000),-np.log10(100),-np.log10(10),-np.log10(1),-np.log10(0.1),-np.log10(0.01)])
    ax.set_yticklabels(['1000','100','10','1','0.1','0.01'])
    ax.set_ylabel('Pressure (hPa)')
    ax.set_title(titlestr, fontsize=16)
    ax.set_xlabel('Latitude $^{\circ}$N')

    return ax

def plotlatlogpre_100to0p01(fig, data, lat, pre, ci, cmin, cmax, titlestr, x1=0.1, x2=0.9, y1=0.1, y2=0.9):
    """
    Plot a pressure versus latitude contour plot up to 0.01hPa.
    """

    # set up contour levels and color map
    nlevs = (cmax-cmin)/ci + 1
    clevs = np.arange(cmin, cmax+ci, ci)
    mymap = mycolors.blue2red_cmap(nlevs)

    plt.rcParams['font.size'] = '12'
    
    ax = fig.add_axes([x1, y1, x2-x1, y2-y1])

    ax.contourf(lat,-1.*np.log10(pre), data, levels=clevs, cmap=mymap, extend='max')
    ax.contour(lat,-1.*np.log10(pre), data, levels=clevs, colors='black', linewidths=0.5)
    ax.set_ylim(-np.log10(100.),-np.log10(0.01))
    ax.set_yticks([-np.log10(100),-np.log10(10),-np.log10(1),-np.log10(0.1),-np.log10(0.01)])
    ax.set_yticklabels(['100','10','1','0.1','0.01'])
    ax.set_ylabel('Pressure (hPa)')
    ax.set_title(titlestr, fontsize=16)
    ax.set_xlabel('Latitude $^{\circ}$N')

    return ax




def plotlatlogpre_to0p01_sayc(fig, data, lat, pre, clevs, titlestr, x1=0.1, x2=0.9, y1=0.1, y2=0.9):
    """
    Plot a pressure versus latitude contour plot up to 0.01hPa.
    Specify contour levels directly rather than a min and max
    """

    # set up contour levels and color map
    nlevs = len(clevs)
    mymap = mycolors.blue2red_cmap(nlevs)

    plt.rcParams['font.size'] = '12'
    
    ax = fig.add_axes([x1, y1, x2-x1, y2-y1])

    ax.contourf(lat,-1.*np.log10(pre), data, levels=clevs, cmap=mymap, extend='max')
    ax.contour(lat,-1.*np.log10(pre), data, levels=clevs, colors='black', linewidths=0.5)
    ax.set_ylim(-np.log10(1000.),-np.log10(0.01))
    ax.set_yticks([-np.log10(1000),-np.log10(100),-np.log10(10),-np.log10(1),-np.log10(0.1),-np.log10(0.01)])
    ax.set_yticklabels(['1000','100','10','1','0.1','0.01'])
    ax.set_ylabel('Pressure (hPa)')
    ax.set_title(titlestr, fontsize=16)

    return ax





def plotqbowinds(fig, data, time, pre, ci, cmin, cmax, titlestr, x1=None, x2=None, y1=None, y2=None):
    """
    Plots a QBO time series as a function of time and log(pressure) 
    """

    # set up contour levels and color map
    nlevs = (cmax-cmin)/ci + 1
    clevs = np.arange(cmin, cmax+ci, ci)
    mymap = mycolors.blue2red_cmap(nlevs)

    plt.rcParams['font.size'] = '12'

    if (x1):
        ax = fig.add_axes([x1, y1, x2-x1, y2-y1])
    else:
        ax = fig.add_axes()

    ax.contourf(time,-1.*np.log10(pre),data, levels=clevs, cmap=mymap, extend='max')
    ax.set_ylim(-np.log10(1000.),-np.log10(1))
    ax.set_yticks([-np.log10(1000),-np.log10(300),-np.log10(100),-np.log10(30),-np.log10(10),
                   -np.log10(3),-np.log10(1)])
    ax.set_yticklabels(['1000','300','100','30','10','3','1'])
    ax.set_ylabel('Pressure (hPa)')
    ax.set_title(titlestr, fontsize=16)
    

    return ax

def plotddamp(fig, data, pre, expname, x1=None, x2=None, y1=None, y2=None, color=None, oplot=False, ax=None):
    """ 
    Plot up the Dunkerton and Delisi amplitude of the QBO.
    Inputs:
        fig = the figure page
        data = the dunkerton and delisi amplitude data
        pre = the pressure axis of data
        expname = the name of the experiment (for legend)
        x1 = the bottom edge of the figure (in units of fractions of the page)
        x2 = the right edge of the figure (in units of fraction of the page)
        y1 = the bottom edge of the figure (in units of fractions of the page)
        y2 = the top edge of the figure ( in units of fractions of the page)
        oplot = if True, only over plot a line
    """

    # if overplotting, check for axis input
    if (oplot and (not ax)):
        print("This isn't going to work.  If overplotting, specify axis")
        sys.exit()

    plt.rcParams['font.size'] = '14'

    if not oplot:
        if (x1):
            ax = fig.add_axes([x1, y1, x2-x1, y2-y1])
        else:
            ax = fig.add_axes()

        ax.set_ylim(-np.log10(100),-np.log10(3))
        ax.set_yticks([-np.log10(100),-np.log10(30),-np.log10(10),-np.log10(3)])
        ax.set_yticklabels(['100','30','10','3'])
        ax.set_ylabel('Pressure (hPa)', fontsize=16)
        ax.set_xlabel('Dunkerton and Delisi amplitude (ms$^{-1}$)',fontsize=16)
        ax.set_title('QBO amplitude', fontsize=16)

    
    if (color):
        ax.plot(np.array(data),-1.*np.log10(np.array(pre)),linewidth=3,label=expname, color=color)
    else:
        ax.plot(np.array(data),-1.*np.log10(np.array(pre)),linewidth=3,label=expname)
 
    return ax

def plotprofile_logp_100to0p01(fig, data, pre, expname, x1=None, x2=None, y1=None, y2=None, color=None, oplot=False, 
                              ax=None, title=None, xtitle=None, xlim=None):
    """
    Plot a vertical profile of data from log(100) to log(0.01)
    Inputs:
        fig = the figure page
        data = the pressure axis of the data
        expname = the name of the experiemnt (for legend)
        x1 = the bottom edge of the figure (in units of fractions of the page)
        x2 = the right edge of the figure (in units of fraction of the page)
        y1 = the bottom edge of the figure (in units of fractions of the page)
        y2 = the top edge of the figure ( in units of fractions of the page)
        oplot = if True, only over plot a line
        ax = the figure axis (needed for overplotting
        xtitle = the title of the x axis
    """
    # if overplotting, check for axis input
    if (oplot and (not ax)):
        print("This isn't going to work.  If overplotting, specify axis")
        sys.exit()

    plt.rcParams['font.size'] = '14'

    if not oplot:
        if (x1):
            ax = fig.add_axes([x1, y1, x2-x1, y2-y1])
        else:
            ax = fig.add_axes()

    ax.set_ylim(-np.log10(100),-np.log10(0.01))
    ax.set_yticks([-np.log10(100),-np.log10(10),-np.log10(1),-np.log10(0.1),-np.log10(0.01)])
    ax.set_yticklabels(['100','10','1','0.1','0.01'])
    ax.set_ylabel('Pressure (hPa)', fontsize=16)

    if (xtitle):
        ax.set_xlabel(xtitle)
  
    if (title):
        ax.set_title(title)

    if (color):
        ax.plot(np.array(data),-1.*np.log10(np.array(pre)),linewidth=3,label=expname, color=color)
    else:
        ax.plot(np.array(data),-1.*np.log10(np.array(pre)),linewidth=3,label=expname)

    if (xlim):
        ax.set_xlim(xlim)

    return ax

def plotprofile_logp_0p1to0p01(fig, data, pre, expname, x1=None, x2=None, y1=None, y2=None, color=None, oplot=False, 
                              ax=None, title=None, xtitle=None, xlim=None):
    """
    Plot a vertical profile of data from log(100) to log(0.01)
    Inputs:
        fig = the figure page
        data = the pressure axis of the data
        expname = the name of the experiemnt (for legend)
        x1 = the bottom edge of the figure (in units of fractions of the page)
        x2 = the right edge of the figure (in units of fraction of the page)
        y1 = the bottom edge of the figure (in units of fractions of the page)
        y2 = the top edge of the figure ( in units of fractions of the page)
        oplot = if True, only over plot a line
        ax = the figure axis (needed for overplotting
        xtitle = the title of the x axis
    """
    # if overplotting, check for axis input
    if (oplot and (not ax)):
        print("This isn't going to work.  If overplotting, specify axis")
        sys.exit()

    plt.rcParams['font.size'] = '14'

    if not oplot:
        if (x1):
            ax = fig.add_axes([x1, y1, x2-x1, y2-y1])
        else:
            ax = fig.add_axes()

    ax.set_ylim(-np.log10(0.1),-np.log10(0.01))
    ax.set_yticks([-np.log10(0.1),-np.log10(0.03),-np.log10(0.01)])
    ax.set_yticklabels(['0.1','0.03','0.01'])
    ax.set_ylabel('Pressure (hPa)', fontsize=16)

    if (xtitle):
        ax.set_xlabel(xtitle)
  
    if (title):
        ax.set_title(title)

    if (color):
        ax.plot(np.array(data),-1.*np.log10(np.array(pre)),linewidth=3,label=expname, color=color)
    else:
        ax.plot(np.array(data),-1.*np.log10(np.array(pre)),linewidth=3,label=expname)

    if (xlim):
        ax.set_xlim(xlim)

    return ax



def plotposneghisto(fig, data, binmin, binmax, binint, titlestr, xtitlestr, x1, x2, y1, y2, 
                   yrange=[0,100],xticks=None, xticknames=None):
    """
    ???? 
    """
    ax = fig.add_axes([x1, y1, x2-x1, y2-y1])

    plt.rcParams['font.size'] = '12'

    binvals = np.arange(binmin, binmax, binint)
    histovals, binedges = np.histogram(data, bins=binvals)
    histovals = (histovals/np.size(data))*100.
    binedges = binedges[0:np.size(binedges)-1]

    ax.bar(binedges[np.where(binedges >= 0)], histovals[np.where(binedges >=0)], 
       width=binedges[1]-binedges[0], bottom=0, align='edge', color='darkred', edgecolor='black')
    ax.bar(binedges[np.where(binedges < 0)], histovals[np.where(binedges < 0)],  
       width=binedges[1]-binedges[0], bottom=0, align='edge', color='royalblue',edgecolor='black')

    ax.set_xlim(binmin,binmax)
    ax.set_ylim(yrange)
    ax.set_title(titlestr)
    ax.set_ylabel('%')
    ax.set_xlabel(xtitlestr)

    if (xticks):
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticknames)


    return ax














