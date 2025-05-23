import numpy as np
import matplotlib.pyplot as plt

# Parameters for the sine wave
frequency = 10  # Frequency in Hertz
amplitude = 10  # Amplitude of the wave
sampling_rate = 30  # Number of samples per second
duration = 10  # Duration in seconds

# Generate the time axis
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
# print(t)
# Generate the sine wave
y = amplitude * np.sin(2 * np.pi * frequency * t) + 10
# print(y)

# Plot the sine wave
plt.plot(t, y)
plt.title(f'Sine Wave: {frequency}Hz')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.tight_layout()
plt.savefig('sine_wave.png')

sine_wave = {
    "timestamps": t,
    "amplitude": y,
}
