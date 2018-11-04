import numpy as np
import scipy.optimize as spopt

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import gridspec

from astropy.stats import sigma_clip

import inspect

import astro_models
import detec_models
import bliss

class signal_params(object):
    # class constructor
    def __init__(self, name='planet', t0=1.97, per=3.19, rp=0.08,
                 a=7, inc=84.2, ecosw=0.1, esinw=0.1, q1=0.001, q2=0.001,
                 fp=0.002, A=0.1, B=0.0, C=0.0, D=0.0, r2=0.08, r2off=0.0, sigF=0.008, mode=''):
        self.name  = name
        self.t0    = t0
        self.per   = per
        self.rp    = rp
        self.a     = a
        self.inc   = inc
        self.ecosw = ecosw
        self.esinw = esinw
        self.q1    = q1
        self.q2    = q2
        self.fp    = fp
        self.A     = A
        self.B     = B
        self.C     = C
        self.D     = D
        self.r2    = r2
        self.r2off = r2off
        self.c1    = 1.0     # Poly coeff 
        self.c2    = 0.0     # Poly coeff 
        self.c3    = 0.0     # Poly coeff 
        self.c4    = 0.0     # Poly coeff 
        self.c5    = 0.0     # Poly coeff 
        self.c6    = 0.0     # Poly coeff 
        self.c7    = 0.0     # Poly coeff 
        self.c8    = 0.0     # Poly coeff 
        self.c9    = 0.0     # Poly coeff 
        self.c10   = 0.0     # Poly coeff 
        self.c11   = 0.0     # Poly coeff 
        self.c12   = 0.0     # Poly coeff 
        self.c15   = 0.0     # Poly coeff 
        self.c13   = 0.0     # Poly coeff 
        self.c14   = 0.0     # Poly coeff 
        self.c16   = 0.0     # Poly coeff 
        self.c17   = 0.0     # Poly coeff 
        self.c18   = 0.0     # Poly coeff 
        self.c19   = 0.0     # Poly coeff 
        self.c20   = 0.0     # Poly coeff 
        self.c21   = 0.0     # Poly coeff 
        self.d1    = 1.0     # PSF width coeff 
        self.d2    = 0.0     # PSF width coeff 
        self.d3    = 0.0     # PSF width coeff 
        self.s1    = 0.0     # step function coeff 
        self.s2    = 0.0     # step function coeff
        self.m1    = 0.0     # tslope coeff 
        self.p1_1  = 1.0     # PLD coefficient
        self.p2_1  = 1.0     # PLD coefficient
        self.p3_1  = 1.0     # PLD coefficient
        self.p4_1  = 1.0     # PLD coefficient
        self.p5_1  = 1.0     # PLD coefficient
        self.p6_1  = 1.0     # PLD coefficient
        self.p7_1  = 1.0     # PLD coefficient
        self.p8_1  = 1.0     # PLD coefficient
        self.p9_1  = 1.0     # PLD coefficient
        self.p10_1 = 0.0     # PLD coefficient
        self.p11_1 = 0.0     # PLD coefficient
        self.p12_1 = 0.0     # PLD coefficient
        self.p13_1 = 0.0     # PLD coefficient
        self.p14_1 = 0.0     # PLD coefficient
        self.p15_1 = 0.0     # PLD coefficient
        self.p16_1 = 0.0     # PLD coefficient
        self.p17_1 = 0.0     # PLD coefficient
        self.p18_1 = 0.0     # PLD coefficient
        self.p19_1 = 0.0     # PLD coefficient
        self.p20_1 = 0.0     # PLD coefficient
        self.p21_1 = 0.0     # PLD coefficient
        self.p22_1 = 0.0     # PLD coefficient
        self.p23_1 = 0.0     # PLD coefficient
        self.p24_1 = 0.0     # PLD coefficient
        self.p25_1 = 0.0     # PLD coefficient        
        self.p1_2  = 0.0     # PLD coefficient
        self.p2_2  = 0.0     # PLD coefficient
        self.p3_2  = 0.0     # PLD coefficient
        self.p4_2  = 0.0     # PLD coefficient
        self.p5_2  = 0.0     # PLD coefficient
        self.p6_2  = 0.0     # PLD coefficient
        self.p7_2  = 0.0     # PLD coefficient
        self.p8_2  = 0.0     # PLD coefficient
        self.p9_2  = 0.0     # PLD coefficient
        self.p10_2 = 0.0     # PLD coefficient
        self.p11_2 = 0.0     # PLD coefficient
        self.p12_2 = 0.0     # PLD coefficient
        self.p13_2 = 0.0     # PLD coefficient
        self.p14_2 = 0.0     # PLD coefficient
        self.p15_2 = 0.0     # PLD coefficient
        self.p16_2 = 0.0     # PLD coefficient
        self.p17_2 = 0.0     # PLD coefficient
        self.p18_2 = 0.0     # PLD coefficient
        self.p19_2 = 0.0     # PLD coefficient
        self.p20_2 = 0.0     # PLD coefficient
        self.p21_2 = 0.0     # PLD coefficient
        self.p22_2 = 0.0     # PLD coefficient
        self.p23_2 = 0.0     # PLD coefficient
        self.p24_2 = 0.0     # PLD coefficient
        self.p25_2 = 0.0     # PLD coefficient
        self.sigF  = sigF
        self.mode  = mode
        self.Tstar = None
        self.TstarUncert = None

def get_data(path, mode):
    '''
    Retrieve binned data
    
    Parameters
    ----------
    
    path : string object
        Full path to the data file output by photometry routine

    Returns
    -------

    flux            : 1D array
        Flux extracted for each frame

    time             : 1D array
        Time stamp for each frame

    xdata            : 1D array
        X-coordinate of the centroid for each frame

    ydata            : 1D array
        Y-coordinate of the centroid for each frame   

    psfwx            : 1D array
        X-width of the target's PSF for each frame     

    psfwy            : 1D array
    Y-width of the target's PSF for each frame     
    '''
    
    if 'pld' in mode.lower():
        if '3x3' in mode.lower():
            flux     = np.loadtxt(path, usecols=np.arange(9), skiprows=1)        # MJy/str
            flux_err = np.loadtxt(path, usecols=np.arange(9,18), skiprows=1)     # MJy/str
            time     = np.loadtxt(path, usecols=[18], skiprows=1)     # BMJD
            xdata    = np.loadtxt(path, usecols=[20], skiprows=1)     # pixel
            ydata    = np.loadtxt(path, usecols=[22], skiprows=1)     # pixel
            psfxwdat = np.loadtxt(path, usecols=[24], skiprows=1)     # pixel
            psfywdat = np.loadtxt(path, usecols=[26], skiprows=1)     # pixel
        elif '5x5' in mode.lower():
            flux     = np.loadtxt(path, usecols=np.arange(25), skiprows=1)       # mJr/str
            flux_err = np.loadtxt(path, usecols=np.arange(25,50), skiprows=1)    # mJr/str
            time     = np.loadtxt(path, usecols=[50], skiprows=1)     # BMJD
            xdata    = np.loadtxt(path, usecols=[52], skiprows=1)     # pixel
            ydata    = np.loadtxt(path, usecols=[54], skiprows=1)     # pixel
            psfxwdat = np.loadtxt(path, usecols=[56], skiprows=1)     # pixel
            psfywdat = np.loadtxt(path, usecols=[58], skiprows=1)     # pixel
        else:
            print('Error: only 3x3 and 5x5 boxes for PLD are supported.')
    else:
    #Loading Data
        flux     = np.loadtxt(path, usecols=[0], skiprows=1)     # mJr/str
        flux_err = np.loadtxt(path, usecols=[1], skiprows=1)     # mJr/str
        time     = np.loadtxt(path, usecols=[2], skiprows=1)     # BMJD
        xdata    = np.loadtxt(path, usecols=[4], skiprows=1)     # pixel
        ydata    = np.loadtxt(path, usecols=[6], skiprows=1)     # pixel
        psfxwdat = np.loadtxt(path, usecols=[8], skiprows=1)     # pixel
        psfywdat = np.loadtxt(path, usecols=[10], skiprows=1)    # pixel

        factor = 1/(np.median(flux))
        flux = factor*flux
        flux_err = factor*flux
    return flux, flux_err, time, xdata, ydata, psfxwdat, psfywdat

def get_full_data(path, mode):
    if 'pld' in mode.lower():
        if '3x3' in mode.lower():
            flux     = np.loadtxt(path, usecols=np.arange(9), skiprows=1)        # MJy/str
            time     = np.loadtxt(path, usecols=[9], skiprows=1)     # BMJD
            xdata    = np.loadtxt(path, usecols=[10], skiprows=1)     # pixel
            ydata    = np.loadtxt(path, usecols=[11], skiprows=1)     # pixel
            psfxw    = np.loadtxt(path, usecols=[12], skiprows=1)     # pixel
            psfyw    = np.loadtxt(path, usecols=[13], skiprows=1)     # pixel
            
        elif '5x5' in mode.lower():
            flux     = np.loadtxt(path, usecols=np.arange(25), skiprows=1)       # mJr/str
            time     = np.loadtxt(path, usecols=[25], skiprows=1)     # BMJD
            xdata    = np.loadtxt(path, usecols=[26], skiprows=1)     # pixel
            ydata    = np.loadtxt(path, usecols=[27], skiprows=1)     # pixel
            psfxw    = np.loadtxt(path, usecols=[28], skiprows=1)     # pixel
            psfyw    = np.loadtxt(path, usecols=[29], skiprows=1)     # pixel
        else:
            print('Error: only 3x3 and 5x5 boxes for PLD are supported.')
        return flux, time, xdata, ydata, psfxw, psfyw
    
    else:
        #Loading Data
        flux     = np.loadtxt(path, usecols=[0], skiprows=1)     # mJr/str
        flux_err = np.loadtxt(path, usecols=[1], skiprows=1)     # mJr/str
        time     = np.loadtxt(path, usecols=[2], skiprows=1)     # hours
        xdata    = np.loadtxt(path, usecols=[3], skiprows=1)     # pixels
        ydata    = np.loadtxt(path, usecols=[4], skiprows=1)     # pixels
        psfxw    = np.loadtxt(path, usecols=[5], skiprows=1)     # pixels
        psfyw    = np.loadtxt(path, usecols=[6], skiprows=1)     # pixels
    
        #remove bad values so that BLISS mapping will work
        mask = np.where(np.logical_and(np.logical_and(np.logical_and(np.isfinite(flux), np.isfinite(flux_err)), 
                                                      np.logical_and(np.isfinite(xdata), np.isfinite(ydata))),
                                       np.logical_and(np.isfinite(psfxw), np.isfinite(psfyw))))

        return flux[mask], flux_err[mask], time[mask], xdata[mask], ydata[mask], psfxw[mask], psfyw[mask]

def clip_full_data(FLUX, FERR, TIME, XDATA, YDATA, PSFXW, PSFYW, nFrames=64, cut=0, ignore=[]):
    # chronological order
    index = np.argsort(TIME)
    FLUX  = FLUX[index]
    TIME  = TIME[index]
    XDATA = XDATA[index]
    YDATA = YDATA[index]
    PSFXW = PSFXW[index]
    PSFYW = PSFYW[index]

    # crop the first AOR (if asked)
    FLUX  = FLUX[int(cut*nFrames):]
    TIME  = TIME[int(cut*nFrames):]
    XDATA = XDATA[int(cut*nFrames):]
    YDATA = YDATA[int(cut*nFrames):]
    PSFXW = PSFXW[int(cut*nFrames):]
    PSFYW = PSFYW[int(cut*nFrames):]

    # Sigma clip per data cube (also masks invalids)
    FLUX_clip  = sigma_clip(FLUX, sigma=6, iters=1)
    XDATA_clip = sigma_clip(XDATA, sigma=6, iters=1)
    YDATA_clip = sigma_clip(YDATA, sigma=3.5, iters=1)
    PSFXW_clip = sigma_clip(PSFXW, sigma=6, iters=1)
    PSFYW_clip = sigma_clip(PSFYW, sigma=3.5, iters=1)

    # Clip bad frames
    ind = np.array([])
    for i in ignore:
        ind = np.append(ind, np.arange(i, len(FLUX), nFrames))
    mask_id = np.zeros(len(FLUX))
    mask_id[ind.astype(int)] = 1
    mask_id = np.ma.make_mask(mask_id)

    # Ultimate Clipping
    MASK  = FLUX_clip.mask + XDATA_clip.mask + YDATA_clip.mask + PSFXW_clip.mask + PSFYW_clip.mask + mask_id
    #FLUX  = np.ma.masked_array(FLUX, mask=MASK)
    #XDATA = np.ma.masked_array(XDATA, mask=MASK)
    #YDATA = np.ma.masked_array(YDATA, mask=MASK)
    #PSFXW = np.ma.masked_array(PSFXW, mask=MASK)
    #PSFYW = np.ma.masked_array(PSFYW, mask=MASK)
    
    #remove bad values so that BLISS mapping will work
    FLUX  = FLUX[np.logical_not(MASK)]
    TIME  = TIME[np.logical_not(MASK)]
    XDATA = XDATA[np.logical_not(MASK)]
    YDATA = YDATA[np.logical_not(MASK)]
    PSFXW = PSFXW[np.logical_not(MASK)]
    PSFYW = PSFYW[np.logical_not(MASK)]

    # normalizing the flux
    FLUX  = FLUX/np.ma.median(FLUX)
    return FLUX, TIME, XDATA, YDATA, PSFXW, PSFYW

def time_sort_data(flux, flux_err, time, xdata, ydata, psfxw, psfyw, cut=0):
    # sorting chronologically
    index      = np.argsort(time)
    time0      = time[index]
    flux0      = flux[index]
    flux_err0  = flux_err[index]
    xdata0     = xdata[index]
    ydata0     = ydata[index]
    psfxw0     = psfxw[index]
    psfyw0     = psfyw[index]

    # chop dithered-calibration AOR
    time       = time0[cut:]
    flux       = flux0[cut:]
    flux_err   = flux_err0[cut:]
    xdata      = xdata0[cut:]
    ydata      = ydata0[cut:]
    psfxw      = psfxw0[cut:]
    psfyw      = psfyw0[cut:]
    return flux, flux_err, time, xdata, ydata, psfxw, psfyw

def expand_dparams(dparams, mode):
    if 'ellipse' not in mode.lower():
        dparams = np.append(dparams, ['r2', 'r2off'])
    elif 'offset' not in mode.lower():
        dparams = np.append(dparams, ['r2off'])

    if 'v2' not in mode.lower():
        dparams = np.append(dparams, ['C', 'D'])

    if 'poly' not in mode.lower():
        dparams = np.append(dparams, ['c'+str(int(i)) for i in range(22)])  
    elif 'poly2' in mode.lower():
        dparams = np.append(dparams, ['c7','c8', 'c9', 'c10', 'c11', 
                                      'c12', 'c13', 'c14', 'c15', 'c16', 
                                      'c17','c18', 'c19', 'c20', 'c21'])
    elif 'poly3' in mode.lower():
        dparams = np.append(dparams, ['c11', 'c12', 'c13', 'c14', 'c15', 'c16', 
                                      'c17','c18', 'c19', 'c20', 'c21'])
    elif 'poly4' in mode.lower():
        dparams = np.append(dparams, ['c16', 'c17','c18', 'c19', 'c20', 'c21'])
        
    if 'ecosw' in dparams and 'esinw' in dparams:
        dparams = np.append(dparams, ['ecc', 'anom', 'w'])
        
    if 'psfw' not in mode.lower():
        dparams = np.append(dparams, ['d1', 'd2', 'd3'])
        
    if 'hside' not in mode.lower():
        dparams = np.append(dparams, ['s1', 's2'])
        
    if 'tslope' not in mode.lower():
        dparams = np.append(dparams, ['m1'])
        
    if 'pld' not in mode.lower():
        dparams = np.append(dparams, ['p1_1', 'p2_1', 'p3_1', 'p4_1', 'p5_1', 'p6_1', 'p7_1', 'p8_1', 
                                      'p9_1', 'p10_1', 'p11_1', 'p12_1', 'p13_1', 'p14_1', 'p15_1', 
                                      'p16_1', 'p17_1', 'p18_1', 'p19_1', 'p20_1', 'p21_1', 'p22_1', 
                                      'p23_1', 'p24_1', 'p25_1', 'p1_2', 'p2_2', 'p3_2', 'p4_2', 'p5_2', 
                                      'p6_2', 'p7_2', 'p8_2', 'p9_2', 'p10_2', 'p11_2', 'p12_2', 'p13_2',
                                      'p14_2', 'p15_2', 'p16_2', 'p17_2', 'p18_2','p19_2', 'p20_2', 
                                      'p21_2', 'p22_2', 'p23_2', 'p24_2', 'p25_2'])
    elif 'pld' in mode.lower():
        if 'pld1' in mode.lower():
            dparams = np.append(dparams, ['p1_2', 'p2_2', 'p3_2', 'p4_2', 'p5_2', 'p6_2', 'p7_2', 'p8_2', 
                                          'p9_2', 'p10_2', 'p11_2', 'p12_2', 'p13_2', 'p14_2', 'p15_2', 
                                          'p16_2', 'p17_2', 'p18_2','p19_2', 'p20_2', 'p21_2', 'p22_2', 
                                          'p23_2', 'p24_2', 'p25_2'])
            if '3x3' in mode.lower():
                dparams = np.append(dparams, ['p10_1', 'p11_1', 'p12_1', 'p13_1', 'p14_1', 'p15_1', 
                                              'p16_1', 'p17_1', 'p18_1', 'p19_1', 'p20_1', 'p21_1',
                                              'p22_1', 'p23_1', 'p24_1', 'p25_1'])
        elif 'pld2' in mode.lower():
            if '3x3' in mode.lower():
                dparams = np.append(dparams, ['p10_1', 'p11_1', 'p12_1', 'p13_1', 'p14_1', 'p15_1', 
                                      'p16_1', 'p17_1', 'p18_1', 'p19_1', 'p20_1', 'p21_1', 'p22_1', 
                                      'p23_1', 'p24_1', 'p25_1', 'p10_2', 'p11_2', 'p12_2', 'p13_2',
                                      'p14_2', 'p15_2', 'p16_2', 'p17_2', 'p18_2','p19_2', 'p20_2', 
                                      'p21_2', 'p22_2', 'p23_2', 'p24_2', 'p25_2'])
    return dparams

def get_lparams(function):
    return inspect.getargspec(function).args

def get_p0(lparams, fancyNames, dparams, obj):
    nparams = np.array([sa for sa in lparams if not any(sb in sa for sb in dparams)])
    fancyLabels = np.array([fancyNames[i] for i in range(len(lparams)) if not any(sb in lparams[i] for sb in dparams)])
    p0 = np.empty(len(nparams))
    for i in range(len(nparams)):
         p0[i] = eval('obj.'+ nparams[i])
    return p0, nparams, fancyLabels

def load_past_params(path):
    '''
    Params:
    -------
    path     : str
        path to the file containing past mcmc result (must be a table saved as .npy)


    '''
    return


def make_lambdafunc(function, dparams=[], obj=[], debug=False):
    '''
    Create a lambda function called dynamic_funk that will fixed the parameters listed in
    dparams with the values in obj.

    Params:
    -------
    function     : str
        name of the original function.
    dparams      : list (optional)
        list of all input parameters the user does not wish to fit. 
        Default is none.
    obj          : str (optional)
        bject containing all initial and fixed parameter values.
        Default is none.
    debug        : bool (optional)
        If true, will print mystr so the user can read the command because executing it.
    
    Return:
    -------
    dynamic_funk : function
        lambda function with fixed parameters.

    Note:
    -----
    The module where the original function is needs to be loaded here.
    '''
    module   = function.__module__
    namefunc = function.__name__
    # get list of params you wish to fit
    lparams  = np.asarray(inspect.getargspec(function).args)
    index    = np.in1d(lparams, dparams)
    nparams  = lparams[np.where(index==False)[0]]
    # assign value to fixed variables
    varstr  = ''
    for label in lparams:
        if label in dparams and label != 'r2':
            tmp = 'obj.' + label
            varstr += str(eval(tmp)) + ', '
        elif label in dparams and label == 'r2':
            varstr += 'rp' + ', '
        else:
            varstr += label + ', '
    #remove extra ', '
    varstr = varstr[:-2]
    
    # generate the line to execute
    mystr = 'global dynamic_funk; dynamic_funk = lambda '
    for i in range(len(nparams)):
        mystr = mystr + nparams[i] +', '
    #remove extra ', '
    mystr = mystr[:-2]
    #mystr = mystr +': '+namefunc+'(' + varstr + ')'
    if module == 'helpers':
        mystr = mystr +': '+namefunc+'(' + varstr + ')'
    else: 
        mystr = mystr +': '+module+'.'+namefunc+'(' + varstr + ')'
    # executing the line
    exec(mystr)
    if debug:
        print(mystr)
    return dynamic_funk

def lnlike(p0, signalfunc, signal_input):
    '''
    Notes:
    ------
    Assuming that we are always fitting for the photometric scatter (sigF). 
    '''
    flux = signal_input[0]
    inv_sigma = 1/p0[-1] #using inverse sigma since multiplying is faster than dividing
    
    # define model
    model = signalfunc(signal_input, *p0)
    return -0.5*np.sum((flux-model)**2)*inv_sigma**2 + flux.size*np.log(inv_sigma)

def lnprob(p0, signalfunc, lnpriorfunc, signal_input, checkPhasePhis, lnpriorcustom='none'):
    '''
    Calculating log probability of the signal function with input parameters p0 and 
    input_data to describe flux.

    Params:
    -------

    '''
    lp = lnpriorfunc(*p0, signal_input[-1], checkPhasePhis)

    if (lnpriorcustom!='none'):
        lp += lnpriorcustom(p0)
    if not np.isfinite(lp):
        return -np.inf
    return lp + lnlike(p0, signalfunc, signal_input)

def lnprior(t0, per, rp, a, inc, ecosw, esinw, q1, q2, fp, A, B, C, D, r2, r2off,
            c1,  c2,  c3,  c4,  c5,  c6, c7,  c8,  c9,  c10, c11, c12, c13, c14, c15,
            c16, c17, c18, c19, c20, c21, p1_1 ,p2_1 ,p3_1 ,p4_1 ,p5_1 ,p6_1 ,p7_1 ,p8_1 ,
            p9_1,p10_1,p11_1,p12_1,p13_1,p14_1,p15_1,p16_1,p17_1,p18_1,p19_1,p20_1,p21_1,
            p22_1,p23_1,p24_1,p25_1,p1_2 ,p2_2 ,p3_2 ,p4_2 ,p5_2 ,p6_2 ,p7_2 ,p8_2 ,p9_2,
            p10_2,p11_2,p12_2,p13_2,p14_2,p15_2,p16_2,p17_2,p18_2,p19_2,p20_2,p21_2,p22_2,
            p23_2,p24_2,p25_2,d1, d2, d3, s1, s2, m1, sigF, mode, checkPhasePhis):
    # checking that the parameters are physically plausible
    check = astro_models.check_phase(checkPhasePhis, A, B, C, D)
    if ((0 < rp < 1) and (0 < fp < 1) and (0 < q1 < 1) and (0 < q2 < 1) and
        (-1 < ecosw < 1) and (-1 < esinw < 1) and (check == False) and (sigF > 0)
        and (m1 > -1)):
        return 0.0
    else:
        return -np.inf

def walk_style(ndim, nwalk, samples, interv, subsamp, labels, fname=None):
    '''
    input:
        ndim    = number of free parameters
        nwalk   = number of walkers
        samples = samples chain
        interv  = take every 'interv' element to thin out the plot
        subsamp = only show the last 'subsamp' steps
    '''
    # get first index
    beg   = len(samples[0,:,0]) - subsamp
    end   = len(samples[0,:,0]) 
    step  = np.arange(beg,end)
    step  = step[::interv] 
    
    # number of columns and rows of subplots
    ncols = 4
    nrows = int(np.ceil(ndim/ncols))
    sizey = 2*nrows
    
    # plotting
    plt.figure(figsize = (15, 2*nrows))
    for ind in range(ndim):
        plt.subplot(nrows, ncols, ind+1)
        mu_param = np.mean(samples[:,:,ind][:,beg:end:interv], axis = 0)
        std_param = np.std(samples[:,:,ind][:,beg:end:interv], axis = 0)
        plt.plot(step, mu_param)
        plt.fill_between(step, mu_param + 3*std_param, mu_param - 3*std_param, facecolor='k', alpha = 0.1)
        plt.fill_between(step, mu_param + 2*std_param, mu_param - 2*std_param, facecolor='k', alpha = 0.1)
        plt.fill_between(step, mu_param + 1*std_param, mu_param - 1*std_param, facecolor='k', alpha = 0.1)
        plt.title(labels[ind])
        plt.xlim(np.min(step), np.max(step))
        if ind < (ndim - ncols):
            plt.xticks([])
        else: 
            plt.xticks(rotation=25)
    if fname != None:
        plt.savefig(fname, bbox_inches='tight')
    else:
        plt.show()
    return    

def chi2(data, fit, err):
    return np.sum(((data - fit)/err)**2)

def loglikelihood(data, fit, err):       
    return -0.5*chi2(data, fit, err) - len(fit)*np.log(err) - len(fit)*np.log(np.sqrt(2*np.pi))

def evidence(logL, Npar, Ndat):
    return logL - (Npar/2)*np.log(Ndat)

def BIC(logL, Npar, Ndat):
    return -2*(logL - (Npar/2)*np.log(Ndat))

def triangle_colors(data1, data2, data3, data4, label, path):
    fig = plt.figure(figsize = (8,8))
    gs  = gridspec.GridSpec(len(data1)-1,len(data1)-1)
    i = 0
    for k in range(np.sum(np.arange(len(data1)))):
        j= k - np.sum(np.arange(i+1))
        ax = fig.add_subplot(gs[i,j])
        ax.plot(data1[j], data1[i+1],'k.', markersize = 0.2)
        l1 = ax.plot(data2[j], data2[i+1],'.', color = '#66ccff', markersize = 0.7, label='$1^{st}$ secondary eclipse')
        l2 = ax.plot(data3[j], data3[i+1],'.', color = '#ff9933', markersize = 0.7, label='transit')
        l3 = ax.plot(data4[j], data4[i+1],'.', color = '#0066ff', markersize = 0.7, label='$2^{nd}$ secondary eclipse')
        if (j == 0):
            plt.setp(ax.get_yticklabels(), rotation = 45)
            ax.yaxis.set_major_locator(MaxNLocator(5, prune = 'both'))
            ax.set_ylabel(label[i+1])
        else:
            plt.setp(ax.get_yticklabels(), visible=False)
        if (i == len(data1)-2):
            plt.setp(ax.get_xticklabels(), rotation = 45)
            plt.axhline(y=0, color='k', linestyle='dashed')
            #ax.plot(bins[j], res[j], '.', color='#ff5050', markersize = 3)  # plot bin residual
            ax.xaxis.set_major_locator(MaxNLocator(5, prune = 'both'))
            ax.set_xlabel(label[j])
        else:
            plt.setp(ax.get_xticklabels(), visible=False)
        if(i == j):
            i += 1
    handles = [l1,l2,l3]
    fig.subplots_adjust(hspace=0)
    fig.subplots_adjust(wspace=0)
    fig.savefig(path, bbox_inches='tight')
    return

def binValues(values, binAxisValues, nbin, assumeWhiteNoise=False):
    bins = np.linspace(np.min(binAxisValues), np.max(binAxisValues), nbin)
    digitized = np.digitize(binAxisValues, bins)
    binned = np.array([np.nanmedian(values[digitized == i]) for i in range(1, nbin)])
    binnedErr = np.mean(np.array([np.nanstd(values[digitized == i]) for i in range(1, nbin)]))
    if assumeWhiteNoise:
        binnedErr /= np.sqrt(len(values)/nbin)
    return binned, binnedErr

def binnedNoise(x, y, nbin):
    bins = np.linspace(np.min(x), np.max(x), nbin)
    digitized = np.digitize(x, bins)
    y_means = np.array([np.nanmean(y[digitized == i]) for i in range(1, nbin)])
    return np.nanstd(y_means)

def getIngressDuration(p0_mcmc, p0_labels, p0_obj, intTime):
    if 'rp' in p0_labels:
        rpMCMC = p0_mcmc[np.where(p0_labels == 'rp')[0][0]]
    else:
        rpMCMC = p0_obj.rp
    if 'a' in p0_labels:
        aMCMC = p0_mcmc[np.where(p0_labels == 'a')[0][0]]
    else:
        aMCMC = p0_obj.a
    if 'per' in p0_labels:
        perMCMC = p0_mcmc[np.where(p0_labels == 'per')[0][0]]
    else:
        perMCMC = p0_obj.per

    return (2*rpMCMC/(2*np.pi*aMCMC/perMCMC))/intTime #Eclipse/transit ingress time

def getOccultationDuration(p0_mcmc, p0_labels, p0_obj, intTime):
    if 'rp' in p0_labels:
        rpMCMC = p0_mcmc[np.where(p0_labels == 'rp')[0][0]]
    else:
        rpMCMC = p0_obj.rp
    if 'a' in p0_labels:
        aMCMC = p0_mcmc[np.where(p0_labels == 'a')[0][0]]
    else:
        aMCMC = p0_obj.a
    if 'per' in p0_labels:
        perMCMC = p0_mcmc[np.where(p0_labels == 'per')[0][0]]
    else:
        perMCMC = p0_obj.per

    return (2/(2*np.pi*aMCMC/perMCMC))/intTime #Transit/eclipse duration