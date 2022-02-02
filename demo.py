import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from spec2rgb import spec2lines

# Get data
#data = pd.read_csv("data/simulated_a_spec.csv")
#lam = np.array(data['wavelength [nm]'])
#intensity = 1-np.array(data["absorbance"])

lam = np.linspace(380, 750, 1000)
intensity = 1.0 * np.ones_like(lam)

img = np.zeros((3, len(intensity), 3))
img[0,:,:] = spec2lines(lam, intensity, colors="good")
img[1,:,:] = spec2lines(lam, intensity, colors="scientific")
img[2,:,:] = spec2lines(lam, intensity, colors="colorful")

#Plotting
plt.imshow(img, aspect='auto', extent=[lam[0],lam[-1],0,1], interpolation='none')
#plt.plot(lam, rgb_man[0,:], color="red")
#plt.plot(lam, rgb_man[1,:], color="green")
#plt.plot(lam, rgb_man[2,:], color="blue")
plt.show()