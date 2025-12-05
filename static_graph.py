import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv(r'D:\PyCharm_ssau\radiotech\lab1\samples_sign_only.txt', sep=r'\s+', header=None)
data1 = pd.read_csv(r'D:\PyCharm_ssau\radiotech\lab1\samples_noise.txt', sep=r'\s+', header=None)
#data.columns = ['frequency_Hz', 're', 'im', 'a', 'b']
data.columns = ['frequency_Hz', 'w', 'd']
data1.columns = ['frequency_Hz1', 'w1', 'd1']
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 6))

axes[0].plot(data['frequency_Hz'], (10 * (np.log10(data['w'] / data1['w1']))))
#axes[0].set_title('dependence power, W on frequency, Hz')
axes[0].set_xlabel('frequency, Hz')
#axes[0].set_ylabel('power, W')

"""axes[1].plot(data['frequency_Hz'], data['d'])
axes[1].set_title('dependence power, D on frequency, Hz')
axes[1].set_xlabel('frequency, Hz')
axes[1].set_ylabel('power, D')"""

plt.suptitle("dependency graph from .txt")

plt.show()
