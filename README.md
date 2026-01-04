# Practical Analysis of Signal Reconstruction
### Digital Signal Processing | Mini-Project

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 👥 Group Contributors
This project was developed as a collaborative effort by:
* **Ayalkibet Teketel**
* **Atsedemariam  Asemaraw**
* **Bamlak Tadesse**
* **Eyosias Tiruneh**
* **Lemi Negeso**

---

## 📌 Project Overview
This repository contains an interactive Digital Signal Processing (DSP) application designed to analyze and visualize the **Whittaker-Shannon Sampling Theorem**. The tool allows users to sample a simulated analog signal and reconstruct it using two primary methods:
1. **Zero-Order Hold (ZOH):** A staircase reconstruction simulating standard DAC behavior.
2. **Sinc Interpolation:** An ideal mathematical reconstruction using the Whittaker-Shannon interpolation formula.

The application provides real-time feedback on signal fidelity, spectral imaging, and the phenomenon of **Aliasing** when the Nyquist criterion is violated.

## 🚀 Key Features
- **Interactive Laboratory:** Real-time sliders to manipulate signal frequency ($f$) and sampling frequency ($F_s$).
- **Automated Nyquist Monitoring:** Integrated logic that flags aliasing risks immediately in the UI.
- **Dual-Domain Analysis:**
    - **Time-Domain:** A master plot comparing Ground Truth, Samples, ZOH, and Sinc interpolation.
    - **Frequency-Domain:** Power Spectral Density (PSD) analysis to observe spectral images and filtering effects.
- **Compliance Visualization:** Custom plotting engine following strict technical requirements:
    - `Ground Truth`: Thin Black Line
    - `Discrete Samples`: Red 'o' Markers
    - `ZOH`: Blue Staircase
    - `Sinc`: Green "Connect-the-dots" Line
- **Engineering Export:** Feature to download high-resolution PNG plots for technical reporting.

---

## 🛠️ System Architecture
The project is built with a modular architecture to ensure a clear separation between mathematical logic and user interface:

```text
dsp-reconstruction-app/
├── app.py              # Main Entry Point (Streamlit UI & Reactive Logic)
├── core/
│   ├── engine.py       # DSP Engine (Vectorized math for Sinc/ZOH)
│   └── __init__.py     # Package initialization
├── plots/              # Directory for exported analysis images
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

---

## 📖 Theoretical Background
The core of this project is the **Whittaker-Shannon Interpolation Formula**:

$$x(t) = \sum_{n=-\infty}^{\infty} x[n] \cdot \text{sinc}\left(\frac{t - nT_s}{T_s}\right)$$

While the Sinc method provides an "ideal" low-pass filter to recover the signal, the ZOH method introduces high-frequency noise (spectral images) due to its rectangular pulse nature in the time domain. This app visualizes these concepts through both visual waveforms and PSD analysis.

---

## 💻 Installation & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/Lemiti/dsp-signal-reconstruction.git
cd dsp-reconstruction-analysis
```

### 2. Set Up Environment
We recommend using a virtual environment:
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

---

## 📊 Analysis Examples
*(Tip: Replace these placeholders with your exported PNGs from the app)*
![[plots/time_domain_reconstruction_50Hz.png|400]]  ![[plots/frequency_domain_analysis_25Hz.png|400]] ![[plots/time_domain_reconstruction_15Hz.png|600]]

| Scenario | Observation |
| :--- | :--- |
| **Oversampling ($F_s > 5f$)** | High fidelity; Sinc tracks Ground Truth perfectly. |
| **Nyquist Boundary ($F_s \approx 2f$)** | ZOH shows significant staircase distortion; Sinc remains accurate. |
| **Aliasing ($F_s < 2f$)** | Frequency folding occurs; original signal is unrecoverable. |

---

## 📜 Acknowledgments
Developed for the **DSP** Mini-Project. Special thanks to our instructor **Ms. Yiwab** for inspiration on giving this project.

***

### Senior Architect's Final Checklist for you:
*   [ ] **GIF/Image:** Ensure you add at least one screenshot of the app to the "Analysis Examples" section.
*   [ ] **License:** I included an MIT license badge. If you don't have a license file yet, you can add one easily through GitHub's UI.
*   [ ] **GitHub Links:** Update the clone URL once your repo is live.

**Congratulations, Team!** This is a project you should all be very proud to show off. Ready to push to GitHub?