"""astro functions for performing derredening"""
from __future__ import (division, print_function, unicode_literals)
from collections import OrderedDict
from astropy.io import fits
import pandas as pd


def Schlafly_dereddening(band, E_B_minus_V, band_name, R_V=3.1):
    """performs dereddening by band.
    :param band: float or numpy array, the band to be derreddened
    :param E_B_minus_V: float or numpy array, E (B-V) value
    :param band_name: string, currently support "g", "r", "i"
    :param R_V: float (optional),
                Fitzpatrick reddening law best-fit coefficient is used
                if not supplied

    :note: Reference from Schlafly E. 2010 et al. appendix Table 6.
    :math: $m_{true} = m_{obs} - redden_coeff * E(B-V)$

    """

    if band_name == "g" and R_V == 3.1:
        redden_coeff = 3.303
    elif band_name == "r" and R_V == 3.1:
        redden_coeff = 2.285
    elif band_name == "i" and R_V == 3.1:
        redden_coeff = 1.698
    else:
        raise NotImplementedError("Currently supported band_name = 'g', 'r'" +
                                  " or 'i'")

    return band - redden_coeff * E_B_minus_V


def fits_cat_to_h5(dataPath):
    """
    path = string, full path to Subaru fits catalog

    """
    cats = OrderedDict({band: fits.open(dataPath + "{0}.cat".format(band))
                        for band in ["I", "R", "G"]})
    df_list = OrderedDict({band: pd.DataFrame(cats[band][2].data.tolist(),
                           columns=cats[band][2].data.dtype.names)
                           for band in cats.keys()})
    for band in df_list.keys():
        df_list[band].to_hdf(dataPath + "preprocessed_subaru_cat.h5",
                             band + "_data")
