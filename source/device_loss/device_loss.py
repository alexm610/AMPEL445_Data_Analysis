import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt

"""
MZIdelta1, from chip2 measurement on July 9, 2023
"""
Iman_MZIdelta1 = '/Users/alexmanak/Dropbox/Alex measurements/Iman_chip7_v2/chip2/09_Jul_2023/09_Jul_2023_00_08_21/Iman_MZIdelta1.mat'
Alex_alignW1 = '/Users/alexmanak/Dropbox/Alex measurements/Iman_chip7_v2/chip2/09_Jul_2023/09_Jul_2023_00_08_21/Alex_alignW1.mat'
MZIdelta1 = loadmat(Iman_MZIdelta1)
alignW1 = loadmat(Alex_alignW1)

"""
Extract data from matfile
"""
data_MZI = MZIdelta1['scandata']
data_GC = alignW1['scandata']

lambda_list = data_MZI['wavelength']
GC_power = data_GC['power']
device_power = data_MZI['power']

gc = GC_power[0][0][:,1]
fibre1 = device_power[0][0][:,0]
wavelength = lambda_list[0][0][0]

"""
Subtract grating coupler loss
"""
device_loss = np.subtract(fibre1, gc)

"""
Plot data
"""
plt.figure()
plt.plot(wavelength*1000000000, gc) # wavelengths are recorded in nm, so multiply by 1e9 for ease of viewing
plt.plot(wavelength*1000000000, fibre1)
plt.plot(wavelength*1000000000, device_loss)
plt.xlim((1470,1580))
plt.xlabel('Wavelength (nm)')
plt.ylabel('Transmission (dB)')
plt.title('Delta1')
plt.show()