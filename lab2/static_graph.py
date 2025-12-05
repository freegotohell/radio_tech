import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

os.chdir(r'D:\PyCharm_ssau\radiotech\lab2')

data = pd.read_csv('samples4.txt', sep='\t', header=None,
                   names=['Frequency', 'Signal', 'Power', 'Inverse', 'LogPower'])

FS = 1.0e6
F = 500000
FMOD = 1000
FFT_POINTS = 10000
DT = 1.0 / FS

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

n_points_show = max(200, len(data))
time = np.arange(len(data)) * DT * 1000
signal_show = data['Signal'].values[:n_points_show]

ax1.plot(time, signal_show, 'b-', linewidth=1)
ax1.set_xlabel('Время, мс')
ax1.set_ylabel('Амплитуда')
ax1.grid(True, alpha=0.3)

mod_period = int(1.0 / FMOD / DT)
n_points_full = max(2 * mod_period, len(data))
time_full = np.arange(len(data)) * DT * 1000
signal_full = data['Signal'].values[:n_points_full]

ax2.plot(time_full, signal_full, 'b-', linewidth=1)
ax2.set_xlabel('Время, мс')
ax2.set_ylabel('Амплитуда')
ax2.grid(True, alpha=0.3)

positive_freq = data['Frequency'] <= FS/2
freq_positive = data['Frequency']#[positive_freq]
power_positive = data['Power']#[positive_freq]

ax3.plot(freq_positive, power_positive, 'r-', linewidth=1)
ax3.set_xlabel('Частота, Гц')
ax3.set_ylabel('Мощность')
ax3.grid(True, alpha=0.3)

ax4.semilogy(freq_positive, power_positive, 'r-', linewidth=1)
ax4.set_xlabel('Частота, Гц')
ax4.set_ylabel('Мощность (лог. шкала)')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()