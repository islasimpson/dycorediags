import matplotlib.pyplot as plt
import numpy as np
from dycoreutils import colormap_utils as mycolors

def get3by3coords():
    """ positioning for 3x3 plots """
    x1 = [0.04,0.37,0.7,0.04,0.37,0.7,0.04,0.37,0.7]
    x2 = [0.31,0.64,0.97,0.31,0.64,0.97,0.31,0.64,0.97]
    y1 = [0.8,0.8,0.8,0.59,0.59,0.59,0.38,0.38,0.38]
    y2 = [0.95,0.95,0.95,0.74,0.74,0.74,0.53,0.53,0.53]

    return x1, x2, y1, y2

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











