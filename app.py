import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from core.engine import ReconstructionEngine

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="DSP Reconstruction Lab", layout="wide")

# --- APP TITLE & DESCRIPTION ---
st.title("📡 Signal Reconstruction Analysis Lab")
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
     ax1.plot(engine.t_analog, x_sinc, color='green', marker='.', markevery=40, label='Sinc (Connect-the-dots)')

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
buf = io.BytesIO()
fig1.savefig(buf, format="png", bbox_inches='tight')
st.download_button(
    label="💾 Download Master Plot as PNG",
    data=buf.getvalue(),
    file_name="time_domain_reconstruction.png",
    mime="image/png"
)

# Repeat for the PSD Plot (fig2)
buf_psd = io.BytesIO()
fig2.savefig(buf_psd, format="png", bbox_inches='tight')
st.download_button(
    label="📊 Download PSD Analysis as PNG",
    data=buf_psd.getvalue(),
    file_name="frequency_domain_analysis.png",
    mime="image/png"
)

# --- PHASE 5: THEORY & ANALYSIS ---
st.divider()
st.header("3. Engineering Analysis & Conclusion")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Time-Domain Insights")
    st.info("""
    **Why the staircase?**  
    The **ZOH (Blue)** reconstruction is a 'sample-and-hold' process. It creates a staircase because it maintains the voltage of a sample until the next clock cycle. This is computationally 'free' but mathematically 'dirty'.
    
    **Why the smooth curve?**  
    **Sinc (Green)** interpolation uses the *Whittaker-Shannon Formula*. It assumes the signal is band-limited and fills the gaps with perfect low-pass filtering. Notice how it tracks the 'Analog' line almost perfectly if Nyquist is met.
    """)

with col2:
    st.subheader("Frequency-Domain Insights")
    st.warning("""
    **Spectral Images in ZOH:**  
    In the Blue PSD, notice the 'bumps' at higher frequencies. These are **Spectral Images** caused by the sharp edges of the staircase. Sharp edges in time = broad frequencies in space.
    
    **The Brick-Wall Filter:**  
    In the Green PSD, the high frequencies are suppressed. The Sinc function acts as an **Ideal Low-Pass Filter**, effectively 'smoothing' out the noise and recovering only the original signal frequency.
    """)

# --- FINAL CONCLUSION FOR THE REPORT ---
with st.expander("📝 View Project Conclusion (Copy for Report)"):
    st.write(f"""
    ### Final Conclusion
    Based on our analysis of a {f_signal}Hz signal sampled at {fs_digital}Hz:
    
    1. **Accuracy:** Sinc interpolation provides superior reconstruction accuracy in the time domain compared to ZOH, which introduces a visible 'staircase' error.
    2. **Spectral Purity:** The Frequency-Domain analysis confirms that ZOH reconstruction suffers from high-frequency harmonic distortion (spectral images). Sinc interpolation significantly attenuates these images, acting as a brick-wall low-pass filter.
    3. **The Nyquist Limit:** When $f_s < 2f$, both methods fail due to **Aliasing**, where high frequencies fold back into the baseband, making the original signal unrecoverable.
    4. **Practicality:** While Sinc is mathematically ideal, it is 'acausal' (requires future samples) and computationally expensive. ZOH remains the standard for initial DAC stages due to its hardware simplicity.
    """)