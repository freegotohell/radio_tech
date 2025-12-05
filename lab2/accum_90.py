import numpy as np
import pandas as pd


def frequency_band_90_power(psd, fs):
    total_power = np.sum(psd)
    k_max = np.argmax(psd)
    power_accum = psd[k_max]

    i = 1
    N = len(psd)

    while power_accum / total_power < 0.9:
        left_index = k_max - i if k_max - i >= 0 else None
        right_index = k_max + i if k_max + i < N else None

        if left_index is not None:
            power_accum += psd[left_index]
        if right_index is not None:
            power_accum += psd[right_index]

        if left_index is None and right_index is None:
            break
        i += 1

    k_low = max(0, k_max - (i - 1))
    k_high = min(N - 1, k_max + (i - 1))

    f_low = k_low * fs / N
    f_high = k_high * fs / N

    return f_low, f_high, power_accum


fs = 1e5
data = pd.read_csv(r'D:\PyCharm_ssau\radiotech\lab2\samples1.txt', sep=r'\s+', header=None)
data.columns = ['Frequency', 'Signal', 'Power', 'Inverse', 'LogPower']
psd1 = np.array(data['Power'])[:len(data['Power'])//2]
psd2 = np.array(data['Power'])[len(data['Power'])//2:]

freq_low1, freq_high1, acc1 = frequency_band_90_power(psd1, fs)
freq_low2, freq_high2, acc2 = frequency_band_90_power(psd2, fs)
print(f"90% power of the 1st peak ({acc1} W) concentrated in the gap [{freq_low1}, {freq_high1}] Hz")
print(f"90% power of the 2nd peak ({acc2} W) concentrated in the gap [{freq_low2}, {freq_high2}] Hz")
