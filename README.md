# 🌍 Urban Environmental Intelligence (2025)

A **Cyberpunk-Themed Streamlit Dashboard** built for real-time global air quality monitoring and diagnostic analysis. This project analyzes a multi-gigabyte dataset utilizing OpenAQ API data to identify environmental anomalies across 100 global sensor nodes.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![Plotly](https://img.shields.io/badge/Plotly-Express-3f4f75)

## 🚀 Features & Analytical Capabilities

The dashboard is structured into four distinct analytical engines:

1. **[📊] Dimensionality Engine (PCA):** 
   Utilizes Principal Component Analysis (`sklearn.decomposition`) to flatten 6-dimensional pollution data (PM2.5, PM10, NO2, Ozone, Temp, Humidity) into a 2D projection, identifying intrinsic cluster separations between Industrial and Residential zones.
   
2. **[📈] High-Density Temporal Analysis:** 
   Processes over 100,000 hourly data points using rolling averages and Hourly × Daily heatmaps to reveal diurnal cycling and short-term anthropogenic pollution events without suffering from overplotting.

3. **[📉] Distribution Models (Hazard Probabilities):** 
   Highlights long-tail extreme hazard events by modeling logarithmic distribution histograms alongside 95th/99th percentile metrics.

4. **[✅] Visual Integrity Audit:** 
   Strict adherence to Tufte's data visualization principles (optimizing Data-Ink ratios). Actively rejects distortive 3D plotting and standardizes on accessible Sequential color mapping.

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mahadbashir1/Urban-Environmental-Intelligence-2025.git
   cd Urban-Environmental-Intelligence-2025
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Dashboard:**
   ```bash
   python -m streamlit run dashboard.py
   ```
   The diagnostic engine will launch locally at `http://localhost:8501`.

## 📁 Repository Structure
- `dashboard.py`: The core Streamlit application containing layout architecture and CSS injection.
- `utils.py`: Data ingestion pipeline for reshaping OpenAQ data from long to wide format utilizing Pandas Pivot Tables.
- `scripts/`: Modularized analytical logic for PCA, temporal patterns, and distribution modeling.
- `data/`: Contains the large temporal raw dataset (excluded via `.gitignore`).
