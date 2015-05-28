""" this script matches and combine spectroscopic members """
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

# note that order of the field matters
sources_df.loc[star_sdss_idxes, "specz"] = np.array(star_df[star_sdss_match].z)
sources_df.loc[star_sdss_idxes, "spec_quality"] = \
    np.array(star_df[star_sdss_match].quality)

# --------- only match spec galaxies with secure redshifts--------
np.sum(spec_df["quality"] == 4)
np.sum(spec_df["quality"] == 3)
accepted_cat = {"quality": [3, 4]}

mask = prep.process_cuts(spec_df, accept_cat=accepted_cat,
                         verbose=True)
spec_df = spec_df[mask]
mask_nan = np.logical_or(np.isnan(spec_df.ra_obj),
                         np.isnan(spec_df.dec_obj))
mask_nan = ~mask_nan
spec_df = spec_df[mask_nan]

# --------- match Subaru with SDSS data ---------------------------
# find nans
subaru_sdss_dist, subaru_sdss_indxes =  \
    prepData.match_catalog(sources_df.Rband_X_WORLD,
                           sources_df.Rband_Y_WORLD,
                           spec_df.ra_obj[mask_nan],
                           spec_df.dec_obj[mask_nan])
# convert dist to arcsec
subaru_sdss_dist = np.abs(subaru_sdss_dist * 60 * 60)
subaru_sdss_match = subaru_sdss_dist < 2.
subaru_sdss_indxes = sources_df.index[subaru_sdss_indxes[subaru_sdss_match]]

no_match = subaru_sdss_dist > 2

sources_df.loc[subaru_sdss_indxes, "specz"] = \
    np.array(spec_df[subaru_sdss_match].z)
sources_df.loc[subaru_sdss_indxes, "spec_quality"] = \
    np.array(spec_df[subaru_sdss_match].quality)

# ----- try to match unmatched data with DEIMOS coordinates------

# subaru_DEIMOS_dist2, subaru_DEIMOS_indxes2 = \
#     prepData.match_catalog(sources_df.Rband_X_WORLD,
#                            sources_df.Rband_Y_WORLD,
#                            spec_df.ra_trace[no_match],
#                            spec_df.dec_trace[no_match])
#
# subaru_DEIMOS_dist2 *= 60 * 60
# subaru_DEIMOS_match = subaru_DEIMOS_dist2 < 2.
# subaru_DEIMOS_indxes = \
#     sources_df.index[subaru_DEIMOS_indxes2[subaru_DEIMOS_match]]
#
# sources_df.loc[subaru_DEIMOS_indxes, "specz"] = \
#   np.array(spec_df[subaru_DEIMOS_match].z)
# sources_df.loc[subaru_DEIMOS_indxes, "spec_quality"] = \
#   np.array(spec_df[subaru_DEIMOS_match].quality)

sources_df.to_hdf(dataPath2 + "combined_cat.h5", "sources_with_specz_df")
