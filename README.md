# Speedlight: NYC Motor Vehicle Collision Analysis

Python-based exploratory data analysis, time-series analysis, and geospatial visualization of traffic collisions in New York City.

# Overview
Speedlight explores patterns in NYC motor vehicle collision records using public data from the New York City Police Department (NYPD). The project examines reported contributing factors, vehicle types, injuries and fatalities, changes over time, and the geographic distribution of crashes. It also uses interactive maps and distance-based filtering to examine collision records around the Queensboro Bridge and Flushing, Queens.

The goal is to turn raw collision records into interpretable statistics, charts, and maps that can support further questions about urban traffic safety.

# Dataset
## Source: NYC Open Data — Motor Vehicle Collisions: Crashes
Provider: New York City Police Department (NYPD)

Each record represents a police-reported motor vehicle collision in NYC. Fields used in the analysis include:
- CRASH DATE, CRASH TIME, and BOROUGH
- LATITUDE and LONGITUDE
- CONTRIBUTING FACTOR VEHICLE 1 and VEHICLE TYPE CODE 1
- Counts of people, pedestrians, cyclists, and motorists injured or killed
To obtain the data: Open the source link, download/export the dataset as a CSV, and save it locally. The original script expects a file named Motor_Vehicle_Collisions_-_Crashes_20250113.csv. If your downloaded filename differs, update the paths in the script.
The source dataset is updated over time. Outputs can vary with the downloaded version and any filtering. This dataset contains reported collisions; it does not, on its own, identify speed-camera installations or establish whether a camera caused changes in crashes.

## Analyses and Visualizations

1. ## Data exploration and quality checks
- Load the CSV into a Pandas DataFrame.
- Inspect descriptive statistics and calculate missing-value counts and percentages for each column.
- Count the most frequent contributing factors and vehicle types in reported crashes.
- Aggregate reported injuries and fatalities across pedestrians, cyclists, and motorists.

2. ## Time-series analysis
- Convert crash dates and times to datetime values.
- Group collision records by hour of day, month, and day to visualize temporal patterns.
- Use statsmodels additive seasonal decomposition with a 365-day period to explore trend, seasonality, and residual components of daily crash counts.
- Plot monthly collision records near Flushing for 2013–2015.

3. ## Geographic analysis
- Compare the number of reported collisions by NYC borough.
- Generate an interactive Folium heatmap using records with available coordinates.
- Create sampled collision-severity maps, distinguishing records involving fatalities, injuries, and neither.
- Apply geodesic-distance filters to examine collisions near the Queensboro Bridge and Flushing.
- Compare collision record counts within a 1 km radius of selected points near Flushing and the Queensboro Bridge.

## Technologies
- Language: Python
- Data processing: Pandas
- Charts: Matplotlib, Seaborn
- Geospatial visualization: Folium
- Geographic distances: GeoPy (geodesic)
- Time-series decomposition: Statsmodels

## Getting Started
1. Get the code and dataset
Download the project code and the CSV from the NYC Open Data dataset page.

If using this project as a Python script, save the analysis code as analysis.py. Place the downloaded CSV in the same directory, or update the input path in the script to match your file location.
2. Install dependencies
python -m pip install pandas matplotlib seaborn folium geopy statsmodels
3. Update data paths
The provided code contains two input paths: a local filename and an absolute Google Colab/Drive path (/content/drive/MyDrive/...). Update both CSV reads to point to the same downloaded file before running outside the original environment.

For example, for a CSV in the project directory:
data = pd.read_csv("Motor_Vehicle_Collisions_-_Crashes_20250113.csv")
4. Run the analysis
python analysis.py
The Matplotlib and Seaborn visualizations are displayed during execution. Three Folium HTML maps are saved to disk (see below). Processing the full dataset, particularly when building the heatmap, may require significant memory and time.
Generated Map Files
The script saves the following interactive maps in the working directory:
File	Description
Heatmap.html	Heatmap of geocoded NYC collision records
severity.html	Sampled NYC collision locations categorized by injury/fatality severity
severity_near_queensboro_bridge.html	Sampled collision locations near the Queensboro Bridge, filtered by geodesic distance


Open the generated .html files in a web browser to explore the maps. Other plots are displayed during execution but are not saved as image files in the current code.

## Methodology Notes and Limitations
- Analyses are based on police-reported collision records, not a complete measure of every traffic incident.
- Some records have missing borough or coordinate values. The mapping steps exclude missing latitude/longitude values.
- The severity maps use random samples (n=1,000 for the citywide map and n=20,000 before Queensboro Bridge filtering; random_state=42) rather than every record.
- The hourly calculation in the original code divides each hour's count by the number of distinct hours, not the number of days. It should not be interpreted as an average number of collisions per day at that hour without revising the calculation.
- Annual seasonal decomposition requires sufficient daily observations (at least two 365-day cycles); handling missing dates may also be necessary for continuous time-series analysis.
- Geographic comparisons use fixed-radius areas around selected coordinates and do not control for traffic volume, exposure, or road conditions.
- No causal conclusions about speed cameras or enforcement effects can be drawn from this script alone; that would require additional installation/enforcement data and a separate research design.

## Data Attribution
Traffic collision data: New York City Police Department (NYPD), via NYC Open Data, Motor Vehicle Collisions — Crashes.

This is an independent exploratory analysis and is not an official NYPD traffic safety report.