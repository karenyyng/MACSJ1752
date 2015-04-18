"""astro functions for performing derredening"""


def Schlafly_dereddening(band, E_B_minus_V, band_name, R_V=3.1):
    """performs dereddening by band.
    :param band: float or numpy array, the band to be derreddened
    :param E_B_minus_V: float or numpy array, E(B-V) value
    :param band_name: string, currently support "g", "r", "i"
    :param R_V: float (optional),
                Fitzpatrick reddening law best-fit coefficient is used
                if not supplied

    :note: Reference from Schlafly E. 2010 et al.

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
    return
