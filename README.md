# Gatun Lake Water Level Monitoring System

**Author:** Jerald Seet Jin  
**Date:** 13/10/2026  

**Live Dashboard:** [https://jeraldseet.github.io/gatun-lake-live-monitor-v2/](https://jeraldseet.github.io/gatun-lake-live-monitor-v2/)

## Executive Summary
An institutional-grade, automated monitoring dashboard designed to track Panama Canal freshwater levels and visualize transit capacity restrictions in real-time. 

Built for commodity traders and freight analysts, this tool automatically scrapes 10-minute high-resolution data alongside macro historical trends to forecast Neopanamax draft restrictions, daily vessel quotas, and potential supply chain bottlenecks across energy, grain, and container markets.

## Key Features

###  Desk-Optimized UI/UX
* **Split-Pane Architecture:** Designed with a 75/25 grid layout inspired by professional trading terminals to separate trend visualization from high-density numerical readouts.
* **TradingView-Style Timeframes:** Toggleable views (1D, 3D, 1W, 1M, 1Y) dynamically adjust the Y-axis to highlight intraday momentum while preserving the ability to zoom out and analyze multi-year seasonal drought cycles.
* **Crosshair Data Inspector:** Interactive hover state provides millisecond-accurate historical readings, dynamically updating operational impact metrics without obscuring the chart.
* **Dynamic Risk Matrix:** Visually maps live water elevation directly to the Panama Canal Authority's (ACP) 6-tier operational threshold matrix (Ideal to Critical).

### Automated Dual-Feed Data Architecture
The backend relies entirely on serverless automation via GitHub Actions to maintain two distinct datasets, optimizing browser performance and chart rendering:
* **Micro-Trend Feed (`live_feed.csv`):** A Python scraper (`monitor.py`) fetches high-resolution data at 10-minute intervals, maintaining a 7-day rolling window for short-term momentum analysis.
* **Macro-Trend Feed (`Download_Gatun_Lake_Water_Level_History.csv`):** A secondary Python script (`daily_append_historical.py`) runs via a scheduled cron job at the end of each day, appending the absolute latest live reading to a historical dataset extending back decades. 
* **In-Memory Stitching:** JavaScript seamlessly merges the static historical data with the live intra-day feed to ensure the 1M and 1Y charts never lag behind real-time market conditions.

## Market Context: Why Gatun Lake Matters
Unlike sea-level canals, the Panama Canal relies on the Gatun lake sitting 85 feet above sea level. Every vessel transit consumes roughly 52 million gallons of water. During prolonged dry seasons or El Niño events, water levels plummet, forcing the ACP to enforce strict draft reductions and transit quotas. 

By tracking the exact buffer between the current water level and the 84-foot "Watch Zone" or 80-foot "Severe Zone," traders can forecast freight rate spikes, rerouting economics (e.g., Cape of Good Hope diversions), and supply constraints before they are officially announced.
