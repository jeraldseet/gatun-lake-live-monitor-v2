# Gatun Lake Water Level Monitoring System

**Author:** Jerald Seet Jin  
**Date:** 13/10/2026  

**Live Dashboard:** [https://jeraldseet.github.io/gatun-lake-live-monitor-v2/](https://jeraldseet.github.io/gatun-lake-live-monitor-v2/)

## Executive Summary
An institutional-grade, automated monitoring dashboard designed to track Panama Canal freshwater levels and visualize transit capacity restrictions in real-time. 

Built for commodity traders and freight analysts, this tool automatically scrapes 10-minute high-resolution data alongside macro historical trends to forecast Neopanamax draft restrictions, daily vessel quotas, and potential supply chain bottlenecks across energy, grain, and container markets.

## Key Features

### Desk-Optimized UI/UX
* **Interactive Seasonality Forecasting:** A dedicated seasonal mode normalizes over 50 years of historical data onto a static Jan–Dec calendar axis, allowing traders to instantly benchmark live trajectories against the 5-year average and the 2023 El Niño drought crisis.
* **Dynamic Comparative Inspector:** In seasonal mode, the crosshair inspector physically transforms to display real-time spreads (e.g., calculating the exact variance between the live value and the 5-year average), eliminating mental math during rapid market analysis.
* **Split-Pane Architecture:** Designed with a professional trading terminal layout to separate trend visualization from high-density numerical readouts.
* **Contextual Risk Matrix:** Visually maps live water elevation directly to the Panama Canal Authority's (ACP) 6-tier operational threshold matrix, explicitly detailing the operational impact (e.g., "Heavy restrictions") and maximum draft limits for each danger zone.

### Automated Serverless Data Architecture
The backend relies entirely on serverless automation via GitHub Actions to maintain three distinct data models, optimizing browser performance and chart rendering:
* **Micro-Trend Feed (`live_feed.csv`):** A Python scraper (`monitor.py`) fetches high-resolution data at 10-minute intervals, maintaining a rolling window for short-term intraday momentum.
* **Macro-Trend Feed (`Download_Gatun_Lake_Water_Level_History.csv`):** A secondary Python script (`daily_append_historical.py`) runs daily to append the absolute latest live reading to a historical dataset extending back to 1965. 
* **[New] Seasonality ETL Engine (`build_seasonality.py`):** A backend aggregation script compiles decades of daily records into a lightweight, pre-calculated `seasonality.json` file, delivering instant historical bands to the frontend without crashing the browser.

## Market Context: Why Gatun Lake Matters
Unlike sea-level canals, the Panama Canal relies on a freshwater reservoir—Gatun Lake—sitting 85 feet above sea level. Every vessel transit consumes roughly 52 million gallons of water. During prolonged dry seasons or severe El Niño events, water levels plummet, forcing the ACP to enforce strict draft reductions and transit quotas. 

By tracking the exact buffer between the current water level and the 84-foot "Watch Zone" or 80-foot "Severe Zone," traders can forecast freight rate spikes, rerouting economics (e.g., Cape of Good Hope diversions), and supply constraints before they are officially announced to the broader market.
