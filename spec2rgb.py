import numpy as np

# Generate image of spectral lines as seen through a spectroscope
# from spectral data.
# lam = vector of wavelengths in [nm]
# intensity = vector of intensies of given wavelengths
# optional: color scheme and custom gamma correction value
def spec2lines(lam, intensity, colors="good", gamma=0.6):
    # Calculate spectrum based on specified conversion method
    if colors == "good":
        rgb = _lam2rgb_good(lam, intensity)
    elif colors == "scientific":
        rgb = _lam2rgb_scientific(lam, intensity)
    elif colors == "colorful":
        rgb = _lam2rgb_colorful(lam, intensity)
    else:
        raise ValueError("Spectrum color type \"" + colors + "\" does not", 
        "exist. Valid values: {\"good\", \"scientific\", \"colorful\"}")
    
    # Apply gammma correction
    rgb **= gamma

    # Convert RGB-matrix to 3 channel 1D image
    img = np.zeros((1, len(intensity), 3))
    img[0,:,0] = rgb[0,:]
    img[0,:,1] = rgb[1,:]
    img[0,:,2] = rgb[2,:]

    return img


# Uneven gaussian function
# s1 = left side standard deviation
# s2 = right side standard deviation
def _g(x, mu, s1, s2):
    res = np.zeros_like(x)
    left = x < mu
    right = x >= mu
    res[left] = np.exp(-0.5*((x[left] - mu)/s1)**2)
    res[right] = np.exp(-0.5*((x[right] - mu)/s2)**2)
    return res

# Function to convert spectral data to rgb vector.
# Color map based on manually fit gaussian functions.
# This is a compromize between accuracy and esthetics.
def _lam2rgb_good(lam, intensity):
    # Manually fitted RGB components
    rbar = 0.35 * _g(lam, 605, 33, 60) \
         + 0.05 * _g(lam, 430, 18, 22)

    gbar = 0.32 * _g(lam, 542, 45, 40)

    bbar = 0.32 * _g(lam, 450, 25, 45)
    
    rgb = np.zeros((3, len(lam)))
    rgb[0,:] = rbar
    rgb[1,:] = gbar
    rgb[2,:] = bbar

    maxval = np.max(rgb)
    for i in range(0,len(intensity)):
        rgb[:,i] *= intensity[i]/maxval
    return rgb


# Function to convert spectral data to rgb vector.
# Colormap based on CIE color matching functions.
# https://en.wikipedia.org/wiki/CIE_1931_color_space
# This is the most accurat choice, but due to limitations in the RGB color
# space colors in the blue-green area cant be displayed correctly.
# To compensate for this, the background color is shifted to gray so that
# the RGB-components are allowed to be "negative".
def _lam2rgb_scientific(lam, intensity):
    xyz = np.zeros((3, len(lam)))
    rgb = np.zeros((3, len(lam)))

    xyz[0,:] =   1.056 * _g(lam, 599.8, 37.9, 31.0) \
               + 0.362 * _g(lam, 442.0, 16.0, 26.7) \
               - 0.065 * _g(lam, 501.1, 20.4, 26.2)

    xyz[1,:] =   0.821 * _g(lam, 568.8, 46.9, 40.5) \
               + 0.286 * _g(lam, 530.9, 16.3, 31.1)

    xyz[2,:] =   1.217 * _g(lam, 437.0, 11.8, 36.0) \
               + 0.681 * _g(lam, 459.0, 26.0, 13.8)
    
    mat = np.matrix([[0.49000, 0.31000, 0.20000],
                     [0.17697, 0.81240, 0.01063],
                     [0.00000, 0.01000, 0.99000]]) \
                    / 0.17697
    
    rgb = np.linalg.solve(mat, xyz)
    
    # Make positive and scale
    interval = np.max(rgb) - np.min(rgb)
    for i in range(0,len(intensity)):
        rgb[:,i] *= intensity[i]/interval
    rgb -= np.min(rgb)

    return rgb

# Function to convert spectral data to rgb vector
# Colormap based on
def _lam2rgb_colorful(lam, intensity):
    rgb = np.zeros((3, len(lam)))

    for i in range(0, len(intensity)): 
        wavelength = lam[i]
        if wavelength >= 380 and wavelength <= 440:
            attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
            R = ((-(wavelength - 440) / (440 - 380)) * attenuation)
            G = 0.0
            B = (1.0 * attenuation)
        elif wavelength >= 440 and wavelength <= 490:
            R = 0.0
            G = ((wavelength - 440) / (490 - 440))
            B = 1.0
        elif wavelength >= 490 and wavelength <= 510:
            R = 0.0
            G = 1.0
            B = (-(wavelength - 510) / (510 - 490))
        elif wavelength >= 510 and wavelength <= 580:
            R = ((wavelength - 510) / (580 - 510))
            G = 1.0
            B = 0.0
        elif wavelength >= 580 and wavelength <= 645:
            R = 1.0
            G = (-(wavelength - 645) / (645 - 580))
            B = 0.0
        elif wavelength >= 645 and wavelength <= 750:
            attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
            R = (1.0 * attenuation)
            G = 0.0
            B = 0.0
        else:
            R = 0.0
            G = 0.0
            B = 0.0
        rgb[0,i] = R * intensity[i]
        rgb[1,i] = G * intensity[i]
        rgb[2,i] = B * intensity[i]
    return rgb