from scipy import signal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Загрузка данных с проверкой количества столбцов
def load_data_with_check(filename):
    """Загрузка данных с автоматическим определением количества столбцов"""
    data = pd.read_csv(filename, sep=r'\s+', header=None)
    print(f"Файл {filename}: {data.shape[1]} столбцов, {data.shape[0]} строк")

    if data.shape[1] == 3:
        data.columns = ['frequency_Hz', 'w', 'd']
    elif data.shape[1] == 4:
        # Если 4 столбца, используем первые три
        data = data.iloc[:, :3]  # Берем первые 3 столбца
        data.columns = ['frequency_Hz', 'w', 'd']
        print(f"  Используются первые 3 столбца из 4")
    else:
        print(f"  Неожиданное количество столбцов: {data.shape[1]}")

    return data


# Загрузка всех файлов
print("Загрузка данных...")
data = load_data_with_check(r'D:\PyCharm_ssau\radiotech\lab1\samples_sign_only.txt')
data1 = load_data_with_check(r'D:\PyCharm_ssau\radiotech\lab1\samples_noise.txt')
data2 = load_data_with_check(r'D:\PyCharm_ssau\radiotech\lab1\samples_sign_noise.txt')

# Визуализация исходных данных
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12, 10))

axes[0].plot(data['frequency_Hz'], data['w'])
axes[0].set_title('Мощность сигнала')
axes[0].set_ylabel('Мощность')
axes[0].grid(True)

axes[1].plot(data1['frequency_Hz'], data1['w'])
axes[1].set_title('Мощность шума')
axes[1].set_ylabel('Мощность')
axes[1].grid(True)

axes[2].plot(data2['frequency_Hz'], data2['w'])
axes[2].set_title('Мощность сигнал+шум')
axes[2].set_ylabel('Мощность')
axes[2].set_xlabel('Частота (Гц)')
axes[2].grid(True)

plt.tight_layout()
plt.show()

# Извлечение данных
power_signal = data['w'].values
power_noise = data1['w'].values
power_total = data2['w'].values
frequencies = data['frequency_Hz'].values


def calculate_detection_threshold(power_signal, power_noise, frequencies, signal_freq=None):
    """
    Расчет порога обнаружения сигнала на основе ваших данных
    """
    # Расчет SNR в dB
    with np.errstate(divide='ignore', invalid='ignore'):
        snr_db = 10 * np.log10(power_signal / power_noise)
    snr_db = np.nan_to_num(snr_db, nan=-100, posinf=100, neginf=-100)

    # Если частота сигнала не задана, находим пик по максимальной мощности сигнала
    if signal_freq is None:
        signal_peak_idx = np.argmax(power_signal)
    else:
        # Ищем ближайшую частоту к заданной
        signal_peak_idx = np.argmin(np.abs(frequencies - signal_freq))

    signal_freq_detected = frequencies[signal_peak_idx]
    signal_peak_power = power_signal[signal_peak_idx]
    signal_peak_snr = snr_db[signal_peak_idx]

    print(f"Обнаружен сигнал на частоте {signal_freq_detected:.2f} Гц")
    print(f"Мощность сигнала: {signal_peak_power:.4f}")
    print(f"SNR сигнала: {signal_peak_snr:.2f} dB")

    # Оценка уровня шума (исключаем область вокруг пика сигнала)
    exclusion_zone = max(10, len(power_signal) // 50)

    noise_indices = []
    if signal_peak_idx - exclusion_zone > 0:
        noise_indices.extend(range(0, signal_peak_idx - exclusion_zone))
    if signal_peak_idx + exclusion_zone < len(power_signal):
        noise_indices.extend(range(signal_peak_idx + exclusion_zone, len(power_signal)))

    if len(noise_indices) > 10:  # Минимум 10 точек для статистики
        noise_power_median = np.median(power_noise[noise_indices])
        noise_std = np.std(power_noise[noise_indices])

        # Порог обнаружения (сигнал должен превышать медиану шума на 5 стандартных отклонений)
        detection_threshold_power = noise_power_median + 5 * noise_std

        # Минимальное SNR, необходимое для обнаружения
        min_snr_linear = detection_threshold_power / noise_power_median
        min_snr_db = 10 * np.log10(min_snr_linear)

        print(f"Медиана мощности шума: {noise_power_median:.4f}")
        print(f"Стандартное отклонение шума: {noise_std:.4f}")
        print(f"Порог обнаружения: {detection_threshold_power:.4f}")
        print(f"Минимальный SNR для обнаружения: {min_snr_db:.2f} dB")

        return min_snr_db, signal_peak_snr
    else:
        print("Недостаточно точек для оценки шума")
        return np.nan, signal_peak_snr


def analyze_snr_vs_fft_synthetic(fft_points_values, signal_amplitude=1.0):
    """
    Анализ зависимости порога обнаружения от количества точек БПФ (синтетические данные)
    """
    results = []

    for n_points in fft_points_values:
        print(f"Анализ для FFT_POINTS = {n_points}")

        # Генерация тестового сигнала
        fs = 1000  # Частота дискретизации
        t = np.arange(n_points) / fs
        f_signal = 50  # Частота сигнала

        # Чистый гармонический сигнал
        clean_signal = signal_amplitude * np.sin(2 * np.pi * f_signal * t)

        # Определение минимального SNR для обнаружения
        min_snr_db = find_detection_threshold_synthetic(clean_signal, n_points, fs, f_signal)

        results.append({
            'fft_points': n_points,
            'min_snr_db': min_snr_db
        })

    return pd.DataFrame(results)


def find_detection_threshold_synthetic(clean_signal, n_points, fs, f_signal, detection_sigma=5):
    """
    Нахождение минимального SNR, при котором сигнал обнаруживается
    """
    snr_values = np.linspace(-30, 10, 20)  # Уменьшим количество точек для скорости
    detection_probability = []

    for snr_db in snr_values:
        detections = 0
        trials = 20  # Уменьшим количество trials для скорости

        for _ in range(trials):
            # Добавление шума с заданным SNR
            noisy_signal = add_noise_with_snr(clean_signal, snr_db)

            # Вычисление БПФ
            fft_result = np.fft.fft(noisy_signal)
            freqs = np.fft.fftfreq(n_points, 1 / fs)
            power_spectrum = np.abs(fft_result) ** 2

            # Поиск сигнала на ожидаемой частоте
            signal_idx = np.argmin(np.abs(freqs - f_signal))
            signal_power = power_spectrum[signal_idx]

            # Оценка мощности шума
            noise_indices = np.concatenate([
                np.arange(max(0, signal_idx - 20), signal_idx - 5),
                np.arange(signal_idx + 5, min(n_points, signal_idx + 20))
            ])

            if len(noise_indices) > 0:
                noise_power = np.median(power_spectrum[noise_indices])
                noise_std = np.std(power_spectrum[noise_indices])

                # Проверка обнаружения
                if signal_power > noise_power + detection_sigma * noise_std:
                    detections += 1

        detection_probability.append(detections / trials)

    # Нахождение SNR с вероятностью обнаружения > 90%
    for i, prob in enumerate(detection_probability):
        if prob >= 0.9:
            return snr_values[i]

    return snr_values[-1]


def add_noise_with_snr(clean_signal, snr_db):
    """
    Добавление шума с заданным SNR
    """
    signal_power = np.mean(clean_signal ** 2)
    noise_power = signal_power / (10 ** (snr_db / 10))
    noise = np.random.normal(0, np.sqrt(noise_power), len(clean_signal))
    return clean_signal + noise


# Основной анализ
print("\n" + "=" * 50)
print("АНАЛИЗ НА ОСНОВЕ ВАШИХ ДАННЫХ")
print("=" * 50)

# Анализ текущих данных
min_snr_required, current_snr = calculate_detection_threshold(power_signal, power_noise, frequencies)

print(f"\nТЕКУЩАЯ СИТУАЦИЯ:")
print(f"Текущий SNR сигнала: {current_snr:.2f} dB")
print(f"Минимальный требуемый SNR для обнаружения: {min_snr_required:.2f} dB")

if current_snr > min_snr_required:
    print("✓ Сигнал ОБНАРУЖИВАЕТСЯ")
else:
    print("✗ Сигнал НЕ обнаруживается")

# Анализ зависимости от FFT точек (синтетические данные)
print("\n" + "=" * 50)
print("АНАЛИЗ ЗАВИСИМОСТИ ОТ FFT_POINTS (Синтетические данные)")
print("=" * 50)

# Используем меньше точек для быстрого анализа
fft_points_range = [1000, 2000, 5000, 10000]  # , 20000, 50000]

results = analyze_snr_vs_fft_synthetic(fft_points_range)

# Построение графиков
plt.figure(figsize=(12, 5))

# График 1: Зависимость минимального SNR от FFT_POINTS
plt.subplot(1, 2, 1)
plt.plot(results['fft_points'], results['min_snr_db'], 'bo-', linewidth=2, markersize=8)
plt.xlabel('Количество точек БПФ (FFT_POINTS)')
plt.ylabel('Минимальное SNR для обнаружения (dB)')
plt.title('Зависимость порога обнаружения от FFT_POINTS')
plt.grid(True, alpha=0.3)
plt.xticks(fft_points_range)

# График 2: Спектры ваших данных
plt.subplot(1, 2, 2)
plt.plot(frequencies, power_signal, 'g-', label='Сигнал', linewidth=2)
plt.plot(frequencies, power_noise, 'r-', label='Шум', alpha=0.7)
plt.plot(frequencies, power_total, 'b-', label='Сигнал+Шум', alpha=0.7)
plt.xlabel('Частота (Гц)')
plt.ylabel('Мощность')
plt.title('Спектры мощности')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Вывод результатов
print("\n" + "=" * 50)
print("РЕЗУЛЬТАТЫ:")
print("=" * 50)
print("Зависимость минимального SNR от FFT_POINTS:")
for _, row in results.iterrows():
    print(f"  FFT_POINTS = {row['fft_points']:6d}: Min SNR = {row['min_snr_db']:6.2f} dB")

print(f"\nВывод: С увеличением количества точек БПФ:")
print(f"  - Улучшается частотное разрешение")
print(f"  - Снижается минимальный detectable SNR")
print(f"  - Улучшается обнаружение слабых сигналов")