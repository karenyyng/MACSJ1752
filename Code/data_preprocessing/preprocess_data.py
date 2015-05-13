"""functions for performing derredening, preprocessing and cuts for
galaxy cluster analysis

See Jee 2013 Cosmic shear paper for suitable cuts for source selection
See Jee 2015 CIZA paper for other cuts
"""
from __future__ import (division, print_function, unicode_literals)
from collections import OrderedDict
import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
import pandas as pd


def calculate_source_count_per_sq_arcmin(lower_left_wcs, upper_right_wcs,
                                         count_in_area):
    if len(lower_left_wcs) != 2 or len(upper_right_wcs) != 2:
        raise ValueError("Inputs need to contain 2 strings of RA and DEC")
    lower_left = SkyCoord(lower_left_wcs[0], lower_left_wcs[1])
    upper_right = SkyCoord(upper_right_wcs[0], upper_right_wcs[1])

    arcmin_sq = np.abs(lower_left.dec.degree - upper_right.dec.degree) * 60 * \
                np.abs(lower_left.ra.degree - upper_right.ra.degree) * 60

    return count_in_area / arcmin_sq


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


def match_catalog(tree_x, tree_y, query_x, query_y, k_neighbor=1):
    """ we make use of scipy.spatial.KDTree.query to
    build a KD tree from tree_x and tree_y coordinates
    then query the nearest neighbor of query_x and query_y

    :param tree_x: numpy array,
    :param tree_y: numpy array, same length as tree_x
    :param query_x: numpy array
    :param query_y: numpy array, same length as query_x

    :note: make sure tree_x, tree_y has same units as query_x and query_y

    :return: [distance, nearest_neighbor_index]
    """
    from scipy import spatial
    # cast everything as a numpy array first
    tree_x = np.array(tree_x)
    tree_y = np.array(tree_y)
    query_x = np.array(query_x)
    query_y = np.array(query_y)

    if len(tree_x) != len(tree_y):
        raise ValueError("Dimension mismatch between tree_x and tree_y")
    if len(query_x) != len(query_y):
        raise ValueError("Dimension mismatch between query_x and query_y")

    tree = spatial.KDTree(np.array([tree_x, tree_y]).transpose())
    pts = np.array([query_x, query_y]).transpose()

    # we use Euclidean distance, p=2
    return tree.query(pts, p=2)

# -------cluster specific utility --------------------


def combine_all_cat_and_save(dataPath="../../Data/Subaru_data/",
                             bands=["I", "R", "G"], filename="combined_cat.h5",
                             out_key="preprocessed_df", save=False):
    """
    :param dataPath:
    """
    cats = OrderedDict({})
    df_dict = OrderedDict({})
    for band in ["I", "R", "G"]:
        cats[band] = fits.open(dataPath + "{0}.cat".format(band))
        df_dict[band] = pd.read_hdf(dataPath + "preprocessed_subaru_cat.h5",
                                    band + "_data")
        df_dict[band].columns = ["{0}band_".format(band) + col
                                 for col in df_dict[band].columns]

    Rshape = fits.open(dataPath + "R.shape")
    Rshapes = pd.DataFrame(Rshape[1].data.tolist(),
                           columns=Rshape[1].data.dtype.names)
    combined_cat = pd.concat([Rshapes, df_dict["R"], df_dict["I"],
                              df_dict["G"]], axis=1)
    if save:
        combined_cat.to_hdf(dataPath + filename, out_key)
    return combined_cat


def fits_cat_to_h5(dataPath, filename="preprocessed_subaru_cat.h5"):
    """
    :param path: full path to Subaru fits catalog

    """
    cats = OrderedDict({band: fits.open(dataPath + "{0}.cat".format(band))
                        for band in ["I", "R", "G"]})
    df_list = OrderedDict({band:
                          pd.DataFrame(cats[band][2].data.tolist(),
                           columns=cats[band][2].data.dtype.names)
                           for band in cats.keys()})
    for band in df_list.keys():
        df_list[band].to_hdf(dataPath + filename,
                             band + "_data")


