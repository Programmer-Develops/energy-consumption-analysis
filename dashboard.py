import pandas as pd
import matplotlib.pyplot as plt
import os
import pathlib
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []
        self.df = pd.DataFrame() 

    def add_readings_from_df(self, df):
        self.df = df
        # Convert rows to MeterReading objects (demonstrating OOP usage)
        for _, row in df.iterrows():
            self.meter_readings.append(MeterReading(row['timestamp'], row['kwh']))

    def calculate_total_consumption(self):
        if self.df.empty:
            return 0.0
        return self.df['kwh'].sum()

    def get_summary_stats(self):
        if self.df.empty:
            return {}
        return {
            'Building': self.name,
            'Total_kWh': self.df['kwh'].sum(),
            'Mean_kWh': self.df['kwh'].mean(),
            'Max_kWh': self.df['kwh'].max(),
            'Min_kWh': self.df['kwh'].min()
        }

class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def add_building(self, name, df_data):
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        self.buildings[name].add_readings_from_df(df_data)

    def get_all_summaries(self):
        summaries = []
        for b_name, b_obj in self.buildings.items():
            b_obj.name = b_name
            summaries.append(b_obj.get_summary_stats())
        return pd.DataFrame(summaries)



def load_data(data_dir='data'):
    all_data = []
    files = list(pathlib.Path(data_dir).glob('*.csv'))
    
    if not files:
        logging.warning(f"No CSV files found in {data_dir}")
        return pd.DataFrame()

    print(f"Found {len(files)} files to process...")

    for file_path in files:
        try:
            df = pd.read_csv(file_path, on_bad_lines='skip')
            
            if 'timestamp' not in df.columns or 'kwh' not in df.columns:
                logging.warning(f"Skipping {file_path.name}: Missing required columns")
                continue

            if 'building_name' not in df.columns:
                df['building_name'] = file_path.stem 
            
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            all_data.append(df)
            logging.info(f"Successfully loaded {file_path.name}")

        except Exception as e:
            logging.error(f"Error loading {file_path.name}: {e}")

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame()

def calculate_daily_totals(df):
    df = df.set_index('timestamp')
    # Group by building and resample
    daily = df.groupby('building_name')['kwh'].resample('D').sum().reset_index()
    return daily

def calculate_weekly_averages(df):
    df = df.set_index('timestamp')
    weekly = df.groupby('building_name')['kwh'].resample('W').mean().reset_index()
    return weekly

def create_dashboard(df_combined, daily_df, weekly_df, output_file='output/dashboard.png'):    
    # Create output directory if needed
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Campus Energy Consumption Dashboard', fontsize=16)
    
    ax1 = axs[0, 0]
    buildings = daily_df['building_name'].unique()
    for b in buildings:
        subset = daily_df[daily_df['building_name'] == b]
        ax1.plot(subset['timestamp'], subset['kwh'], label=b)
    ax1.set_title('Daily Energy Consumption Trend')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Total kWh')
    ax1.legend()
    ax1.grid(True)

    ax2 = axs[0, 1]
    avg_per_building = weekly_df.groupby('building_name')['kwh'].mean()
    avg_per_building.plot(kind='bar', ax=ax2, color='skyblue')
    ax2.set_title('Average Weekly Consumption per Building')
    ax2.set_ylabel('Average kWh')
    ax2.tick_params(axis='x', rotation=45)

    ax3 = plt.subplot(2, 1, 2) 
    df_combined['hour'] = df_combined['timestamp'].dt.hour
    
    for b in buildings:
        subset = df_combined[df_combined['building_name'] == b]
        ax3.scatter(subset['hour'], subset['kwh'], alpha=0.5, label=b)
    
    ax3.set_title('Consumption Distribution by Hour (Peak Load Analysis)')
    ax3.set_xlabel('Hour of Day (0-23)')
    ax3.set_ylabel('kWh Recorded')
    ax3.set_xticks(range(0, 24))
    ax3.legend()
    ax3.grid(True, linestyle='--')

    plt.tight_layout()
    plt.savefig(output_file)
    print(f"Dashboard saved to {output_file}")
    plt.close()

def generate_reports(df_combined, manager, output_dir='output'):
    os.makedirs(output_dir, exist_ok=True)
    
    df_combined.to_csv(f'{output_dir}/cleaned_energy_data.csv', index=False)
    
    summary_df = manager.get_all_summaries()
    summary_df.to_csv(f'{output_dir}/building_summary.csv', index=False)
    
    total_consumption = df_combined['kwh'].sum()
    highest_building = summary_df.loc[summary_df['Total_kWh'].idxmax()]
    
    peak_hour = df_combined.groupby('hour')['kwh'].mean().idxmax()
    
    report_content = f"""
    === CAMPUS ENERGY EXECUTIVE SUMMARY ===
    Total Campus Consumption: {total_consumption:.2f} kWh
    
    Highest Consuming Building:
    - Name: {highest_building['Building']}
    - Total Usage: {highest_building['Total_kWh']:.2f} kWh
    
    Peak Load Analysis:
    - Peak Load Hour (Campus Average): {peak_hour}:00
    
    Building Breakdown:
    {summary_df.to_string(index=False)}
    """
    
    with open(f'{output_dir}/summary.txt', 'w') as f:
        f.write(report_content)
        
    print(report_content) 

def main():
    print("--- Starting Data Ingestion ---")
    df = load_data()
    
    if df.empty:
        print("No data loaded. Exiting.")
        return

    print("--- Building Object Models ---")
    manager = BuildingManager()
    for name, group in df.groupby('building_name'):
        manager.add_building(name, group)

    print("--- Calculating Aggregates ---")
    daily_stats = calculate_daily_totals(df)
    weekly_stats = calculate_weekly_averages(df)

    print("--- Generating Visual Dashboard ---")
    create_dashboard(df, daily_stats, weekly_stats)

    print("--- Saving Reports ---")
    generate_reports(df, manager)
    print("Process Complete.")

if __name__ == "__main__":
    main()