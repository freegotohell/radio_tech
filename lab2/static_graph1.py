import pandas as pd

import matplotlib.pyplot as plt

data = pd.read_csv(r'D:\PyCharm_ssau\radiotech\lab2\samples19.txt', sep=r'\s+', header=None)
data.columns = ['Frequency', 'Signal', 'Power', 'Inverse', 'LogPower']
plt.figure(figsize=(12, 6))

plt.plot(data['Frequency'], data['Power'], 'r-', linewidth=1)
plt.xlabel('frequency, Hz')
plt.ylabel('power, W')
plt.grid(True, alpha=0.3)

plt.show()
