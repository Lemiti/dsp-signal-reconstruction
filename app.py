import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from core.engine import ReconstructionEngine

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="DSP Reconstruction Lab", layout="wide")

# --- APP TITLE & DESCRIPTION ---
st.title("🔬 Signal Reconstruction Analysis Lab")
st.markdown("""
This application demonstrates how a continuous signal is reconstructed from discrete samples 
using **Zero-Order Hold (ZOH)** and **Sinc Interpolation**.
""")

# --- SIDEBAR: CONTROLS ---
st.sidebar.header("🛠️ Signal Parameters")

# 1. Signal Settings
f_signal = st.sidebar.slider("Signal Frequency (Hz)", min_value=1, max_value=20, value=5)
duration = st.sidebar.slider("Observation Window (sec)", min_value=0.1, max_value=2.0, value=0.5, step=0.1)

st.sidebar.divider()

# 2. Sampling Settings
st.sidebar.header("📡 ADC Settings")
fs_digital = st.sidebar.number_input("Sampling Frequency (Fs)", min_value=2, max_value=200, value=25)

# --- SENIOR ARCHITECT LOGIC: NYQUIST VALIDATION ---
nyquist_freq = 2 * f_signal
is_aliased = fs_digital < nyquist_freq

if is_aliased:
    st.sidebar.error(f"⚠️ ALIASING DETECTED\nFs ({fs_digital}Hz) < 2 * f ({nyquist_freq}Hz)")
else:
    st.sidebar.success(f"✅ NYQUIST SATISFIED\nFs ({fs_digital}Hz) > 2 * f ({nyquist_freq}Hz)")

st.sidebar.divider()

# 3. Visibility Toggles
st.sidebar.header("👁️ Visualization Layers")
show_gt = st.sidebar.checkbox("Ground Truth (Analog)", value=True)
show_samples = st.sidebar.checkbox("Discrete Samples", value=True)
show_zoh = st.sidebar.checkbox("ZOH Reconstruction", value=True)
show_sinc = st.sidebar.checkbox("Sinc Interpolation", value=True)

# --- DATA PROCESSING (Recap from Phase 3) ---
engine = ReconstructionEngine(f_signal, fs_digital, duration)
x_analog = engine.get_ground_truth()
x_samples = engine.get_samples()
x_zoh = engine.reconstruct_zoh(x_samples)
x_sinc = engine.reconstruct_sinc(x_samples)

# --- PHASE 4: TIME-DOMAIN ANALYSIS (MASTER PLOT) ---
st.header("1. Time-Domain Analysis")

fig1, ax1 = plt.subplots(figsize=(12, 6))

# 1. Ground Truth (Thin Black Line)
if show_gt:
    ax1.plot(engine.t_analog, x_analog, color='black', linewidth=1, label='Ground Truth (Analog)')

# 2. ZOH Reconstruction (Blue Staircase)
# Rule of Thumb: We use 'plt.step' with 'post' to show the sample being held.
if show_zoh:
    ax1.step(engine.t_samples, x_samples, where='post', color='blue', linewidth=2, label='ZOH Reconstruction')

# 3. Sinc Reconstruction (Green Line)
if show_sinc:
    ax1.plot(engine.t_analog, x_sinc, color='green', linewidth=2, label='Sinc Interpolation')

# 4. Discrete Samples (Red 'o' markers)
if show_samples:
    # We use a stem plot or scatter for samples; requirements asked for red 'o'
    ax1.plot(engine.t_samples, x_samples, 'ro', markersize=6, label='Discrete Samples')

ax1.set_title("Master Plot: Signal Reconstruction Comparison")
ax1.set_xlabel("Time (seconds)")
ax1.set_ylabel("Amplitude")
ax1.legend(loc='upper right')
ax1.grid(True, linestyle='--', alpha=0.7)

st.pyplot(fig1)

# --- PHASE 4: FREQUENCY-DOMAIN ANALYSIS (PSD) ---
st.header("2. Frequency-Domain Analysis")
st.markdown("Analyzing the Power Spectral Density (PSD) to visualize spectral images and filtering effects.")

# Calculate PSDs using our Engine
f_zoh, psd_zoh = engine.get_psd(x_zoh)
f_sinc, psd_sinc = engine.get_psd(x_sinc)

fig2, (psd_ax1, psd_ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Subplot 1: ZOH PSD
psd_ax1.plot(f_zoh, psd_zoh, color='blue')
psd_ax1.set_title("PSD: ZOH Reconstructed Signal")
psd_ax1.set_ylabel("Power/Freq (dB/Hz)")
psd_ax1.set_xlim(0, fs_digital * 3) # View up to 3x sampling freq to see images
psd_ax1.grid(True)

# Subplot 2: Sinc PSD
psd_ax2.plot(f_sinc, psd_sinc, color='green')
psd_ax2.set_title("PSD: Sinc Reconstructed Signal")
psd_ax2.set_xlabel("Frequency (Hz)")
psd_ax2.set_ylabel("Power/Freq (dB/Hz)")
psd_ax2.set_xlim(0, fs_digital * 3)
psd_ax2.grid(True)

plt.tight_layout()
st.pyplot(fig2)



