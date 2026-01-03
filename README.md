# Practical Analysis of Signal Reconstruction

An interactive DSP application built with Python and Streamlit to visualize the 
Whittaker-Shannon Sampling Theorem using Zero-Order Hold (ZOH) and Sinc Interpolation.

## Features
- Dynamic Signal and Sampling Frequency adjustment.
- Real-time Time-Domain visualization (Ground Truth, Samples, ZOH, Sinc).
- Frequency-Domain Analysis via Power Spectral Density (PSD).
- Automated PDF/PNG report generation.

## Installation
1. Clone the repo: `git clone https://github.com/Lemiti/dsp-signal-reconstruction.git`
2. Create venv: `python3 -m venv venv`
3. Activate venv: 
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install requirements: `pip install -r requirements.txt`
5. Run app: `streamlit run app.py`