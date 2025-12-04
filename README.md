# Campus Energy-Use Dashboard

## 1. Project Objective
The primary objective of this Capstone project is to develop an end-to-end data analysis pipeline that assists the campus facilities team in tracking and optimizing electricity usage. By automating the processing of raw meter data, this dashboard provides actionable insights to support administrative decision-making regarding energy efficiency.

Key goals include:
* Ingesting and cleaning raw data from multiple building sources.
* Implementing Object-Oriented Programming (OOP) to model real-world building systems.
* Visualizing trends, peak loads, and comparisons to identify high-consumption areas[cite: 62].

## 2. Dataset Source
The dataset used for this project consists of synthetic meter readings generated to simulate realistic campus energy usage.
* **Location:** The data is located in the `/data/` directory of this repository.
* **Format:** The data consists of multiple `.csv` files (e.g., `building_A.csv`, `building_B.csv`).
* **Structure:** Each file contains the following columns:
    * `timestamp`: The date and time of the recording (YYYY-MM-DD HH:MM:SS).
    * `kwh`: The electricity consumption in Kilowatt-hours.
* **Note:** The script is designed to handle missing files or corrupt data lines during ingestion.

## 3. Methodology
The solution is implemented in Python and follows a modular structure divided into four main stages:

### A. Data Ingestion & Validation
* utilized the `pathlib` library to dynamically detect and loop through all CSV files in the data directory.
* Implemented `pandas` to read files into a master DataFrame, using exception handling (try-except blocks) to manage missing files or invalid data formats.

### B. Object-Oriented Modeling (OOP)
To ensure code scalability and organization, the system is modeled using three primary classes:
1.  **`MeterReading`:** Stores individual timestamp and energy data points.
2.  **`Building`:** Represents a specific building, managing a list of readings and providing methods to calculate total consumption.
3.  **`BuildingManager`:** Orchestrates multiple building objects to generate campus-wide summaries.

### C. Aggregation Logic
* Used Pandas functions such as `.groupby()` and `.resample()` to transform raw data into meaningful time-series insights.
* Calculated metrics including Daily Totals, Weekly Averages, and Peak Hour Loads.

### D. Visualization
* Created a unified dashboard using `matplotlib.pyplot` with `plt.subplots()`.
* The dashboard includes three distinct visualizations:
    1.  **Trend Line:** Displays daily consumption fluctuations over time.
    2.  **Bar Chart:** Compares average weekly usage across different buildings.
    3.  **Scatter Plot:** Maps consumption against the hour of the day to identify peak load times.

## 4. Insights & Outputs
Upon execution, the script generates a textual summary and data exports in the `/output/` folder. Key insights derived from the analysis include:

* **Total Campus Consumption:** A consolidated metric of energy use across all facilities.
* **Highest Consumer:** Identification of the building with the highest total energy draw.
* **Peak Load Time:** Analysis of the specific hour (e.g., 14:00 or 15:00) when campus energy demand is highest.

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