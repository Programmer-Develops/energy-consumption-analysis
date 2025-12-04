# Campus Energy-Use Dashboard

## 1. Project Objective
[cite_start]The primary objective of this Capstone project is to develop an end-to-end data analysis pipeline that assists the campus facilities team in tracking and optimizing electricity usage[cite: 8]. [cite_start]By automating the processing of raw meter data, this dashboard provides actionable insights to support administrative decision-making regarding energy efficiency[cite: 9].

Key goals include:
* [cite_start]Ingesting and cleaning raw data from multiple building sources[cite: 16].
* [cite_start]Implementing Object-Oriented Programming (OOP) to model real-world building systems[cite: 42].
* [cite_start]Visualizing trends, peak loads, and comparisons to identify high-consumption areas[cite: 62].

## 2. Dataset Source
The dataset used for this project consists of synthetic meter readings generated to simulate realistic campus energy usage.
* [cite_start]**Location:** The data is located in the `/data/` directory of this repository.
* **Format:** The data consists of multiple `.csv` files (e.g., `building_A.csv`, `building_B.csv`).
* **Structure:** Each file contains the following columns:
    * `timestamp`: The date and time of the recording (YYYY-MM-DD HH:MM:SS).
    * `kwh`: The electricity consumption in Kilowatt-hours.
* [cite_start]**Note:** The script is designed to handle missing files or corrupt data lines during ingestion[cite: 20].

## 3. Methodology
The solution is implemented in Python and follows a modular structure divided into four main stages:

### A. Data Ingestion & Validation
* [cite_start]utilized the `pathlib` library to dynamically detect and loop through all CSV files in the data directory[cite: 18].
* [cite_start]Implemented `pandas` to read files into a master DataFrame, using exception handling (try-except blocks) to manage missing files or invalid data formats[cite: 19, 20].

### B. Object-Oriented Modeling (OOP)
[cite_start]To ensure code scalability and organization, the system is modeled using three primary classes[cite: 41]:
1.  [cite_start]**`MeterReading`:** Stores individual timestamp and energy data points[cite: 50].
2.  [cite_start]**`Building`:** Represents a specific building, managing a list of readings and providing methods to calculate total consumption[cite: 44, 56].
3.  [cite_start]**`BuildingManager`:** Orchestrates multiple building objects to generate campus-wide summaries[cite: 58].

### C. Aggregation Logic
* [cite_start]Used Pandas functions such as `.groupby()` and `.resample()` to transform raw data into meaningful time-series insights[cite: 34].
* [cite_start]Calculated metrics including Daily Totals, Weekly Averages, and Peak Hour Loads[cite: 39].

### D. Visualization
* [cite_start]Created a unified dashboard using `matplotlib.pyplot` with `plt.subplots()`[cite: 68].
* [cite_start]The dashboard includes three distinct visualizations[cite: 64, 65, 66, 67]:
    1.  **Trend Line:** Displays daily consumption fluctuations over time.
    2.  **Bar Chart:** Compares average weekly usage across different buildings.
    3.  **Scatter Plot:** Maps consumption against the hour of the day to identify peak load times.

## 4. Insights & Outputs
Upon execution, the script generates a textual summary and data exports in the `/output/` folder. Key insights derived from the analysis include:

* [cite_start]**Total Campus Consumption:** A consolidated metric of energy use across all facilities[cite: 79].
* [cite_start]**Highest Consumer:** Identification of the building with the highest total energy draw[cite: 80].
* [cite_start]**Peak Load Time:** Analysis of the specific hour (e.g., 14:00 or 15:00) when campus energy demand is highest[cite: 81].

**Generated Files:**
* `dashboard.png`: The visual dashboard.
* `cleaned_energy_data.csv`: The merged and processed dataset.
* `building_summary.csv`: Aggregated statistics per building.
* `summary.txt`: A concise executive report.

## 5. How to Run
1.  Ensure you have Python installed along with the required libraries:
    ```bash
    pip install pandas matplotlib
    ```
2.  Place your CSV data files in the `data/` folder.
3.  Run the main script:
    ```bash
    python dashboard.py
    ```
4.  Check the `output/` folder for the results.