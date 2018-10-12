
import numpy as np
import matplotlib.pyplot as plt
import helpers

def plot_photometry(time0, flux0, xdata0, ydata0, psfxw0, psfyw0, 
                    time, flux, xdata, ydata, psfxw, psfyw, breaks, savepath, peritime):
    '''
    Makes a multi-panel plot from photometry outputs.
    params:
    -------
        time0 : 1D array 
            array of time stamps. Discarded points not removed.
        flux0 : 1D array
            array of flux values for each time stamps. Discarded points not removed.
        xdata0 : 1D array
            initial modelled the fluxes for each time stamps. Discarded points not removed.
        ydata0: 1D array
            initial modelled astrophysical flux variation for each time stamps. 
            Discarded points not removed.
        psfxw0: 1D array
            Point-Spread-Function (PSF) width along the x-direction. Discarded points not removed.
        psfyw0: 1D array
            Point-Spread-Function (PSF) width along the x-direction. Discarded points not removed.
        time  : 1D array 
            array of time stamps. Discarded points removed.
        flux  : 1D array
            array of flux values for each time stamps. Discarded points removed.
        xdata  : 1D array
            initial modelled the fluxes for each time stamps. Discarded points removed.
        ydata : 1D array
            initial modelled astrophysical flux variation for each time stamps. Discarded points removed.
        psfxw : 1D array
            Point-Spread-Function (PSF) width along the x-direction. Discarded points removed.
        psfyw : 1D array
            Point-Spread-Function (PSF) width along the x-direction. Discarded points removed.
        break : 1D array
            time of the breaks from one AOR to another.
        savepath : str
            path to directory where the plot will be saved
    returns:
    --------
        none
    '''
    
    fig, axes = plt.subplots(5, 1, sharex=True, figsize=(10, 12))
    #fig.suptitle("XO-3b Observation")

    axes[0].plot(time0, flux0,  'r.', markersize=1, alpha = 0.7)
    axes[0].plot(time, flux,  'k.', markersize=2, alpha = 1.0)
    axes[0].set_ylabel("Relative Flux $F$")
    axes[0].set_xlim((np.min(time0), np.max(time0)))

    axes[1].plot(time0, xdata0,  'r.', markersize=1, alpha = 0.7)
    axes[1].plot(time, xdata,  'k.', markersize=2, alpha = 1.0)
    axes[1].set_ylabel("x-centroid $x_0$")

    axes[2].plot(time0, ydata0,  'r.', markersize=1, alpha = 0.7)
    axes[2].plot(time, ydata, 'k.', markersize=2, alpha = 1.0)
    axes[2].set_ylabel("y-centroid $y_0$")

    axes[3].plot(time0, psfxw0,  'r.', markersize=1, alpha = 0.7)
    axes[3].plot(time, psfxw, 'k.', markersize=2, alpha = 1.0)
    axes[3].set_ylabel("x PSF-width $\sigma _x$")

    axes[4].plot(time0, psfyw0,  'r.', markersize=1, alpha = 0.7)
    axes[4].plot(time, psfyw,  'k.', markersize=2, alpha = 1.0)
    axes[4].set_ylabel("y PSF-width $\sigma _y$")
    axes[4].set_xlabel('Time (BMJD)')

    for i in range(5):
        axes[i].axvline(x=peritime, color ='C1', alpha=0.8, linestyle = 'dashed')
        for j in range(len(breaks)):
            axes[i].axvline(x=breaks[j], color ='k', alpha=0.3, linestyle = 'dashed')

    fig.subplots_adjust(hspace=0)
    pathplot = savepath + '01_Raw_data.pdf'
    fig.savefig(pathplot, bbox_inches='tight')
    return


def plot_init_guess(time, data, astro, detec_full, savepath):
    '''
    Makes a multi-panel plots for the initial light curve guesses.
    params:
    -------
        time       : 1D array 
            array of time stamps
        data       : 1D array
            array of flux values for each time stamps
        astro      : 1D array
            initial modelled astrophysical flux variation for each time stamps
        detec_full : 1D array
            initial modelled flux variation due to the detector for each time stamps
        savepath   : str
            path to directory where the plot will be saved
    returns:
    --------
        none
    '''
    
    fig, axes = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(10,9))
    #fig.suptitle('Initial Guess')
    
    axes[0].plot(time, data, '.', label='data')
    axes[0].plot(time, astro*detec_full, '.', label='guess')
    
    axes[1].plot(time, data/detec_full, '.', label='Corrected')
    axes[1].plot(time, astro, '.', label='Astrophysical')
    
    axes[2].plot(time, data/detec_full, '.', label='Corrected')
    axes[2].plot(time, astro, '.', label='Astrophysical')
    axes[2].set_ylim(0.998, 1.005)
    
    axes[3].plot(time, data/detec_full-astro, '.', label='residuals')
    axes[3].axhline(y=0, linewidth=2, color='black')
    
    axes[0].set_ylabel('Relative Flux')
    axes[2].set_ylabel('Relative Flux')
    axes[2].set_xlabel('Time (BMJD)')
    
    axes[0].legend(loc=3)
    axes[1].legend(loc=3)
    axes[2].legend(loc=3)
    axes[3].legend(loc=3)
    axes[3].set_xlim(np.min(time), np.max(time))
    
    fig.subplots_adjust(hspace=0)
    pathplot = savepath + '02_Initial_Guess.pdf'
    fig.savefig(pathplot, bbox_inches='tight')
    return

def plot_psf_dependence(time, flux, detec_guess, astro_guess, psfxw, psfyw, breaks, savepath, peritime):
    fig, axes = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(10,8))

    axes[0].plot(time, flux/detec_guess, '.', label='Corrected Data')
    axes[0].plot(time, astro_guess,'.', label='Astrophysical Guess')
    axes[0].legend(loc=3)
    axes[0].set_ylabel('Flux')

    axes[1].plot(time, flux/detec_guess-astro_guess,'.', label='Residuals')
    axes[1].axhline(y=0, color='C1', linewidth=4)
    axes[1].legend(loc=3)
    axes[1].set_ylabel('Residuals')

    axes[2].plot(time, psfxw, '.')
    axes[2].set_ylabel('X-PSF Width')

    axes[3].plot(time, psfyw, '.')
    axes[3].set_xlim(np.min(time), np.max(time))
    axes[3].set_ylabel('Y-PSF Width')
    axes[3].set_xlabel('Time (BMJD)')

    for i in range(4):
        axes[i].axvline(x=peritime, color ='red', alpha=0.8, linestyle = 'dashed')
        for j in range(len(breaks)):
            axes[i].axvline(x=breaks[j], color ='k', alpha=0.3, linestyle = 'dashed')

    fig.subplots_adjust(hspace=0)
    pathplot = savepath + 'PSF_width_Noise_Correlation.pdf'
    fig.savefig(pathplot)
    return

def plot_bestfit(x, flux, astro, detec, mode, breaks, savepath=None, showplot=True, peritime=-np.inf, nbin=None, fontsize=10):
    
    if nbin is not None:
        x_binned, _ = helpers.binValues(x, x, nbin)
        #raw_flux_binned, flux_binned_err = helpers.binValues(flux, x, nbin)
        calibrated_binned, calibrated_binned_err = helpers.binValues(flux/detec, x, nbin, assumeWhiteNoise=True)
        residuals_binned, residuals_binned_err = helpers.binValues(flux/detec-astro, x, nbin, assumeWhiteNoise=True)
    
    fig, axes = plt.subplots(ncols = 1, nrows = 4, sharex = True, figsize=(8, 14))
    
    axes[0].set_xlim(np.min(x), np.max(x))
    axes[0].plot(x, flux, '.', color = 'k', markersize = 4, alpha = 0.15)
    axes[0].plot(x, astro*detec, '.', color = 'r', markersize = 2.5, alpha = 0.4)
    #axes[0].set_ylim(0.975, 1.0125)
    axes[0].set_ylabel('Raw Flux', fontsize=fontsize)

    axes[1].plot(x, flux/detec, '.', color = 'k', markersize = 4, alpha = 0.15)
    axes[1].plot(x, astro, color = 'r', linewidth=2)
    if nbin is not None:
        axes[1].errorbar(x_binned, calibrated_binned, yerr=calibrated_binned_err, fmt='.',
                         color = 'blue', markersize = 10, alpha = 1)
    axes[1].set_ylabel('Calibrated Flux', fontsize=fontsize)
    # axes[1].set_ylim(ymin=1-3*np.std(flux/detec - astro), ymax=np.max(astro)+4*np.std(flux/detec - astro))
    #axes[1].set_ylim(0.9825, 1.0125)
    
    axes[2].axhline(y=1, color='k', linewidth = 2, linestyle='dashed', alpha = 0.5)
    axes[2].plot(x, flux/detec, '.', color = 'k', markersize = 4, alpha = 0.15)
    axes[2].plot(x, astro, color = 'r', linewidth=2)
    if nbin is not None:
        axes[2].errorbar(x_binned, calibrated_binned, yerr=calibrated_binned_err, fmt='.',
                         color = 'blue', markersize = 10, alpha = 1)
    axes[2].set_ylabel('Calibrated Flux', fontsize=fontsize)
    #axes[2].set_ylim(0.9975, 1.0035)
    # axes[2].set_ylim(ymin=1-3*np.std(flux/detec - astro), ymax=np.max(astro)+4*np.std(flux/detec - astro))
    axes[2].set_ylim(ymin=1-3*np.std(flux/detec - astro))

    axes[3].plot(x, flux/detec - astro, 'k.', markersize = 4, alpha = 0.15)
    axes[3].axhline(y=0, color='r', linewidth = 2)
    if nbin is not None:
        axes[3].errorbar(x_binned, residuals_binned, yerr=residuals_binned_err, fmt='.',
                         color = 'blue', markersize = 10, alpha = 1)
    axes[3].set_ylabel('Residuals', fontsize=fontsize)
    axes[3].set_xlabel('Time from Periapse (days)', fontsize=fontsize)
    # axes[3].set_ylim(-4*np.std(flux/detec - astro), 4*np.std(flux/detec - astro))

    for i in range(len(axes)):
        axes[i].xaxis.set_tick_params(labelsize=fontsize)
        axes[i].yaxis.set_tick_params(labelsize=fontsize)
        axes[i].axvline(x=peritime, color ='C1', alpha=0.8, linestyle = 'dashed')
        for j in range(len(breaks)):
            axes[i].axvline(x=(breaks[j]), color ='k', alpha=0.3, linestyle = 'dashed')
    #fig.align_ylabels()
    
    fig.subplots_adjust(hspace=0)
    
    if savepath is not None:
        plotname = savepath + 'MCMC_'+mode+'_2.pdf'
        fig.savefig(plotname, bbox_inches='tight')
    if showplot:
        plt.show()
    
    return
