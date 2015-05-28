""" this script matches and combine spectroscopic members """
from __future__ import (division, print_function)
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# from astroML.plotting import hist
from DataScienceToolBox import preprocessing as prep
import preprocess_data as prepData

dataPath1 = "/Users/karenyng/Documents/Research/code/" + \
    "RadioRelicData/MACSJ1752/"
dataPath2 = "./../../Data/Subaru_data/"

spec_df = pd.read_csv(dataPath1 + "macs1752_1_2_3_4.csv")
sources_df = pd.read_hdf(dataPath2 + "combined_cat.h5",
                         "preprocess_df")

# brightstar_wcs = (268.06539916992188, 44.668739318847656)

# --------replace non-sensical spec_df values----------------
spec_df.replace(-99.0, np.nan, inplace=True)
spec_df["ra_obj"].replace(139037, np.nan, inplace=True)


# --------match stars ---------------------------------------
stars_mask = np.logical_and(spec_df.quality == -1,
                            spec_df.comment == "star")
star_df = spec_df[stars_mask]

star_dist, star_sdss_idxes = \
    prepData.match_catalog(sources_df.Rband_X_WORLD,
                           sources_df.Rband_Y_WORLD,
                           star_df.ra_obj,
                           star_df.dec_obj,
                           distance_upper_bound=2. / 60. / 60.)

star_dist = np.abs(star_dist * 60 * 60)
# correct for the index of sources_df does not start at 0
# and is not continuous
star_sdss_match = star_dist < 2.
star_sdss_idxes = sources_df.index[star_sdss_idxes[star_sdss_match]]

sources_df["specz"] = np.nan
sources_df["spec_quality"] = np.nan
sources_df["specz_err"] = np.nan

# note that order of the field matters
sources_df.loc[star_sdss_idxes, "specz"] = np.array(star_df[star_sdss_match].z)
sources_df.loc[star_sdss_idxes, "spec_quality"] = \
    np.array(star_df[star_sdss_match].quality)

print ("{0} out of {1} ".format(np.sum(star_sdss_match), star_df.shape[0]) +
       "stars are matched within 2 arcsecs")

# --------- only match spec galaxies with secure redshifts--------
np.sum(spec_df["quality"] == 4)
np.sum(spec_df["quality"] == 3)
accepted_cat = {"quality": [3, 4]}

mask = prep.process_cuts(spec_df, accept_cat=accepted_cat,
                         verbose=True)
spec_df = spec_df[mask]
mask_nan = np.logical_or(np.isnan(spec_df.ra_obj),
                         np.isnan(spec_df.dec_obj))
print ("Spec objects with nan RA or DEC = {}".format(np.sum(mask_nan)))
mask_nan = ~mask_nan
spec_df = spec_df[mask_nan]

# --------- match Subaru with SDSS data ---------------------------
# find nans
subaru_sdss_dist, subaru_sdss_indxes =  \
    prepData.match_catalog(sources_df.Rband_X_WORLD,
                           sources_df.Rband_Y_WORLD,
                           spec_df.ra_obj,
                           spec_df.dec_obj)
# convert dist to arcsec
subaru_sdss_dist = np.abs(subaru_sdss_dist * 60 * 60)
subaru_sdss_match = subaru_sdss_dist < 2.
subaru_sdss_indxes = sources_df.index[subaru_sdss_indxes[subaru_sdss_match]]

no_match = subaru_sdss_dist > 2

# save matched objects
sources_df.loc[subaru_sdss_indxes, "specz"] = \
    np.array(spec_df[subaru_sdss_match].z)
sources_df.loc[subaru_sdss_indxes, "spec_quality"] = \
    np.array(spec_df[subaru_sdss_match].quality)
sources_df.loc[subaru_sdss_indxes, "specz_err"] = \
    np.array(spec_df[subaru_sdss_match].zerr)

print ("{0} out of {1} ".format(np.sum(subaru_sdss_match), spec_df.shape[0]) +
       "galaxies are matched within 2 arcsecs")

# saved objects that we cannot match


# ----- try to match unmatched data with DEIMOS coordinates------

subaru_DEIMOS_dist2, subaru_DEIMOS_indxes2 = \
    prepData.match_catalog(sources_df.Rband_X_WORLD,
                           sources_df.Rband_Y_WORLD,
                           spec_df.ra_trace,
                           spec_df.dec_trace)

subaru_DEIMOS_dist2 *= 60 * 60
subaru_DEIMOS_match = np.logical_and(subaru_DEIMOS_dist2 < 2.,
                                     no_match)
subaru_DEIMOS_indxes = \
    sources_df.index[subaru_DEIMOS_indxes2[subaru_DEIMOS_match]]

sources_df.loc[subaru_DEIMOS_indxes, "specz"] = \
    np.array(spec_df[subaru_DEIMOS_match].z)
sources_df.loc[subaru_DEIMOS_indxes, "spec_quality"] = \
    np.array(spec_df[subaru_DEIMOS_match].quality)
sources_df.loc[subaru_DEIMOS_indxes, "specz_err"] = \
    np.array(spec_df[subaru_DEIMOS_match].zerr)


# append objects that are not matched to dataframe
keys = ["ra_obj", "dec_obj", "z", "zerr", "quality"]
to_append_no_matched = spec_df.loc[no_match, keys].copy()
to_append_no_matched.columns = [
    "Rband_X_WORLD", "Rband_Y_WORLD", "specz",
    "specz_err", "spec_quality"]
sources_df = pd.concat([sources_df, to_append_no_matched], axis=0)

sources_df.to_hdf(dataPath2 + "combined_cat.h5", "sources_with_specz_df")
