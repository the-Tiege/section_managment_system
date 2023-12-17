import math

#This function take latitude and longitude as arguments and returns an irish OS map 10 figure Grid reference.
def OS_GRID(lat, lon):
    """
    Converts latitude and longitude coordinates to an Irish OS map 10-figure grid reference.

    Parameters:
    - lat (float): Latitude in decimal degrees.
    - lon (float): Longitude in decimal degrees.

    Returns:
    - str: Irish OS map 10-figure grid reference.
    """
    deg2rad = math.pi/ 180
    rad2deg = 180.0 / math.pi
    phi = lat * deg2rad      # convert latitude to radians
    lam = lon * deg2rad   # convert longitude to radians

    #Irish OS model
    a = 6377340.189      # OSI semi-major
    b = 6356034.447      # OSI semi-minor
    e0 = 200000          # OSI easting of false origin
    n0 = 250000          # OSI northing of false origin
    f0 = 1.000035        # OSI scale factor on central meridian
    e2 = 0.00667054015   # OSI eccentricity squared
    lam0 = -0.13962634015954636615389526147909  # OSI false east
    phi0 = 0.93375114981696632365417456114141   # OSI false north
    af0 = a * f0
    bf0 = b * f0

    # easting
    slat2 = math.sin(phi) * math.sin(phi)
    nu = af0 / (math.sqrt(1 - (e2 * (slat2))))
    rho = (nu * (1 - e2)) / (1 - (e2 * slat2))
    eta2 = (nu / rho) - 1
    p = lam - lam0
    IV = nu * math.cos(phi)
    clat3 = math.pow(math.cos(phi),3)
    tlat2 = math.tan(phi) * math.tan(phi)
    V = (nu / 6) * clat3 * ((nu / rho) - tlat2)
    clat5 = math.pow(math.cos(phi), 5)
    tlat4 = math.pow(math.tan(phi), 4)
    VI = (nu / 120) * clat5 * ((5 - (18 * tlat2)) + tlat4 + (14 * eta2) - (58 * tlat2 * eta2))
    east = e0 + (p * IV) + (math.pow(p, 3) * V) + (math.pow(p, 5) * VI)

    # northing
    n = (af0 - bf0) / (af0 + bf0)
    M = Marc(bf0, n, phi0, phi)
    I = M + (n0)
    II = (nu / 2) * math.sin(phi) * math.cos(phi)
    III = ((nu / 24) * math.sin(phi) * math.pow(math.cos(phi), 3)) * (5 - math.pow(math.tan(phi), 2) + (9 * eta2))
    IIIA = ((nu / 720) * math.sin(phi) * clat5) * (61 - (58 * tlat2) + tlat4)
    north = I + ((p * p) * II) + (math.pow(p, 4) * III) + (math.pow(p, 6) * IIIA)
    east = round(east)       # round to whole number
    north = round(north)     # round to whole number
    nstr = str(north)      # convert to string
    estr = str(east)      # ditto

    nrg = NE2NGR(east, north)

    #return "Nortings "+ nstr + " Eastings "+ estr + " Grid " + nrg
    return nrg

def Marc(bf0, n, phi0, phi):
    """
    Calculates the Marc term used in the OS_GRID function.

    Parameters:
    - bf0 (float): Calculated constant.
    - n (float): Calculated constant.
    - phi0 (float): False north.
    - phi (float): Latitude in radians.

    Returns:
    - float: Marc term.
  """
    Marc = bf0 * (((1 + n + ((5 / 4) * (n * n)) + ((5 / 4) * (n * n * n))) * (phi - phi0))
    - (((3 * n) + (3 * (n * n)) + ((21 / 8) * (n * n * n))) * (math.sin(phi - phi0)) * (math.cos(phi + phi0)))
    + ((((15 / 8) * (n * n)) + ((15 / 8) * (n * n * n))) * (math.sin(2 * (phi - phi0))) * (math.cos(2 * (phi + phi0))))
    - (((35 / 24) * (n * n * n)) * (math.sin(3 * (phi - phi0))) * (math.cos(3 * (phi + phi0)))))
    return Marc

def NE2NGR(east, north):
    """
    Converts easting and northing values to an Irish OS map 10-figure grid reference.

    Parameters:
    - east (float): Easting value.
    - north (float): Northing value.

    Returns:
    - str: Irish OS map 10-figure grid reference.
    """
    eX = east / 500000
    nX = north / 500000
    tmp = math.floor(eX)-5.0 * math.floor(nX)+17.0
    nX = 5 * (nX - math.floor(nX))
    eX = 20 - 5.0 * math.floor(nX) + math.floor(5.0 * (eX - math.floor(eX)))
    if eX > 7.5:
      eX = eX + 1
    if tmp > 7.5:
      tmp = tmp + 1
    eing = str(east)
    ning = str(north)
    lnth = len(eing)
    eing = eing[lnth - 5:lnth]
    lnth = len(ning)
    ning = ning[lnth - 5:lnth]
    ngr = chr(int(eX) + 65) + " " + eing + " " + ning
    return ngr

