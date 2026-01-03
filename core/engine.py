import numpy as np
from scipy import signal

class ReconstructionEngine:
    def __init__(self, f_signal, fs_digital, duration, fs_analog=2000):
        """
        Initializes the DSP Engine.
        :param f_signal: Frequency of the input sine wave (Hz)
        :param fs_digital: Sampling frequency for our 'ADC' (Hz)
        :param duration: Length of the signal in seconds
        :param fs_analog: High resolution to simulate 'Analog' ground truth
        """
        self.f_signal = f_signal
        self.fs_digital = fs_digital
        self.duration = duration
        self.fs_analog = fs_analog
        self.ts_digital = 1.0 / fs_digital

        # Generate Time Axes
        self.t_analog = np.linspace(0, duration, int(fs_analog * duration), endpoint=False)
        self.t_samples = np.arange(0, duration, self.ts_digital)

    def get_ground_truth(self):
        """Generates the 'perfect' analog signal."""
        return np.sin(2 * np.pi * self.f_signal * self.t_analog)

    def get_samples(self):
        """Generates the discrete samples (The Red 'o' markers)."""
        return np.sin(2 * np.pi * self.f_signal * self.t_samples)

    def reconstruct_zoh(self, samples):
        """
        Zero-Order Hold Reconstruction.
        Rule of Thumb: Each sample is held constant for Ts seconds.
        """
        # We find which sample index corresponds to each analog time point
        indices = np.searchsorted(self.t_samples, self.t_analog, side='right') - 1
        indices = np.clip(indices, 0, len(samples) - 1)
        return samples[indices]

    def reconstruct_sinc(self, samples):
        """
        Whittaker-Shannon Sinc Interpolation.
        Math: x(t) = sum( x[n] * sinc((t - nTs) / Ts) )
        """
        # Matrix Broadcasting for efficiency (Senior Engineer trick)
        # t_analog is (M,), t_samples is (N,)
        # (t_analog - t_samples) creates a (M, N) matrix
        T_s = self.ts_digital
        sinc_matrix = np.sinc((self.t_analog[:, None] - self.t_samples[None, :]) / T_s)
        
        # Matrix multiply the sinc pulses with the sample values
        return np.dot(sinc_matrix, samples)

    def get_psd(self, sig):
        """
        Calculates Power Spectral Density.
        Returns: frequency axis, PSD in dB.
        """
        f, psd = signal.welch(sig, self.fs_analog, nperseg=1024)
        # Convert to dB scale for professional visualization
        psd_db = 10 * np.log10(psd + 1e-12) 
        return f, psd_db