import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from sine_wave import sine_wave
import time

def analyze_wave(heights, timestamps, water_depth):
    """
    Analyze wave data using FFT and shallow water wave speed formula.

    Parameters:
        heights (array-like): Wave height data (in cm).
        timestamps (array-like): Corresponding timestamps (in seconds).
        water_depth (float): Water depth (in meters).

    Returns:
        dict: A dictionary containing frequency, amplitude, and wavelength.
    """
    dt = np.mean(np.diff(timestamps))  # Time interval (assuming uniform spacing)
    
    # Perform Fast Fourier Transform (FFT) to get the frequency components
    N = len(heights)
    yf = fft(heights)  # FFT of the height data
    xf = fftfreq(N, dt)[:N//2]  # Frequencies associated with FFT
    
    # Find the dominant frequency (the peak in the FFT)
    idx_peak = np.argmax(np.abs(yf[:N//2]))  # Index of the peak
    dominant_freq = abs(xf[idx_peak])  # Dominant frequency in Hertz
    
    # Calculate the amplitude (peak value) of the wave
    amplitude = np.max(heights) - np.min(heights)
    
    # Calculate wave speed using shallow water wave speed formula
    g = 9.81  # Acceleration due to gravity (m/s^2)
    wave_speed = np.sqrt(g * water_depth)  # Wave speed in m/s
    
    # Convert wave speed to cm/s (if heights are in cm)
    wave_speed_cm = wave_speed * 100  # 1 m = 100 cm
    
    # Calculate the wavelength using wave speed and dominant frequency
    wavelength = wave_speed_cm / dominant_freq if dominant_freq != 0 else np.inf

    # Plot the time-domain wave (height vs. time)
    plt.figure(figsize=(14, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(timestamps, heights, marker='o', color='b')
    plt.title('Time-Domain Signal (Height vs. Time)')
    plt.xlabel('Time (s)')
    plt.ylabel('Height (cm)')
    
    # Plot the frequency-domain representation (FFT amplitude vs. frequency)
    plt.subplot(1, 2, 2)
    plt.plot(xf, 2.0/N * np.abs(yf[:N//2]), color='r')
    plt.title('Frequency-Domain Signal (FFT)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    
    # Automatically save the plot as PNG
    plt.tight_layout()
    plt.savefig(f'./op/wave_analysis{time.time()}.png')  # Save as PNG file
    # plt.show()

    return {
        'frequency': dominant_freq,   # Frequency in Hz
        'amplitude': amplitude / 2,   # Peak amplitude (from crest to mean)
        'wavelength': wavelength      # Wavelength in cm
    }

# Example usage
if __name__ == "__main__":
    # Generate example wave data (replace with your actual data)
    timestamps = np.linspace(0, 10, 1000)  # 10 seconds, 1000 samples
    heights = sine_wave(timestamps, amplitude=10, frequency=0.5)  # Example sine wave
    
    # Water depth in meters (customize this based on your data context)
    water_depth = 1.0  # 1 meter
    
    # Analyze the wave
    results = analyze_wave(heights, timestamps, water_depth)
    print("Analysis Results:")
    print(f"Dominant Frequency: {results['frequency']} Hz")
    print(f"Amplitude: {results['amplitude']} cm")
    print(f"Wavelength: {results['wavelength']} cm")