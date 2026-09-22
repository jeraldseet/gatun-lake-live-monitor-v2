Gatun Lake Water Level Monitoring System

Author: Jerald Seet Jin  
Date: 31/07/2026  

## 1. Executive Summary
The Gatun Lake automated monitoring system is designed to provide a continuous, autonomous data feed of water levels from the Panama Canal Authority (ACP). Because water levels in Gatun Lake directly impact the draft limits and transit capacity of the Panama Canal, having real-time, accurate data provides a distinct strategic and trading edge.

ACP does not offer a direct, public API. This system acts as a specialized digital worker, built to prioritize speed, accuracy, and 24/7 reliability without requiring manual oversight.

## 2. How It Works (Conceptual)
* **The Trigger:** Every 10 minutes, an external pinger (cron) signals the cloud servers (GitHub) to wake up.
* **The Extraction:** A virtual web browser opens the ACP's interactive dashboard, waits for the latest water level data to load by detecting the "ft" metric, and extracts the exact measurements.
* **The Storage:** The system appends this data to a single continuously running spreadsheet log (`live_feed.csv`) and saves it to the cloud.

### 2.1 Rolling Data Storage
The automated web scraping pipeline runs every 10 minutes (6 runs per hour). To prevent performance degradation during Excel background refreshes, the storage logic is streamlined into a single file managed by Python and Pandas:
* **`live_feed.csv`:** A rolling 3-day window designed exclusively for the live Excel dashboard. It strictly caps the data at 432 rows to ensure lightweight, instantaneous data pulls.

## 3. Business Value & Usage
* **Reduced Manual Effort:** Data is fetched and formatted automatically around the clock.
* **Direct, Anonymous Integration:** The resulting CSV file acts as a clean, standardized data source. With the repository set to Public, the analyst team can pull this data directly into Excel dashboards using Anonymous access via the GitHub "Raw" URL, eliminating password and access token management.
* **Cost Efficiency:** The entire architecture is built on free, enterprise-grade cloud infrastructure.

## 4. System Architecture & Technical Implementation
Built as a serverless, event-driven data pipeline using Python, GitHub Actions, and an external cron webhook. 

### 4.1 Data Extraction (The Scraper)
* **Language & Library:** Python utilizing `playwright` and `pandas`. 
* **Rationale:** The ACP WebPortal renders data using dynamic JavaScript. `playwright` runs a headless browser, allowing background API requests to settle (`wait_until="networkidle"`). The script explicitly waits for the locator `.gaugechart .text-center` containing the text `"ft"` to ensure the DOM is fully loaded before extracting and cleaning the numeric value.

### 4.2 Infrastructure & CI/CD Pipeline
* **Environment:** GitHub Actions hosted runners (Ubuntu).
* **Execution Steps:** Checks out the repository, installs the Python environment/dependencies, executes the Playwright script, and uses Pandas to append new readings while dropping older rows to maintain the strict 432-row limit. It then pushes the updated CSV back to the main branch.

### 4.3 Scheduling, Orchestration, and Security
* **Decoupled Scheduling:** GitHub Actions' native cron shares a global queue, causing execution delays. Scheduling was decoupled to an external service (cron-job.org) sending a precise POST request every 10 minutes to the GitHub REST API via `workflow_dispatch`.
* **Execution Security:** The external cron job authenticates using a Fine-Grained Personal Access Token (PAT) passed securely in the HTTP headers as a Bearer token, scoped strictly for workflow dispatches.
