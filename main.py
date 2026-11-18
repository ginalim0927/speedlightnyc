import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium

data = pd.read_csv("Motor_Vehicle_Collisions_-_Crashes_20250113.csv")
data.head()
desc_stats = data.describe()
desc_stats

# Checking data for missing values
missing_values = data.isnull().sum()
missing_values_percentage = (missing_values / len(data)) * 100
missing_data = pd.DataFrame({'Missing Values': missing_values, 'Percentage (%)': missing_values_percentage})
missing_data.sort_values(by='Percentage (%)', ascending=False)

top_factors = data['CONTRIBUTING FACTOR VEHICLE 1'].value_counts().head(10)

plt.figure(figsize=(12, 7))
# Plotting the top contributing factors, fill in x as the index field of the variable 'top_factors'
sns.barplot(x=top_factors.index, y=top_factors.values, palette="magma")
plt.title('Top 10 Contributing Factors to crashes', fontsize=16)
plt.xlabel('Reasons For Crashing', fontsize=14)
plt.ylabel('Frequency of those Reasons', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Determine the top vehicle types involved in crashes
top_vehicle_types = data['VEHICLE TYPE CODE 1'].value_counts().head(10)

# Plotting the top vehicle types
plt.figure(figsize=(12, 7))
sns.barplot(x=top_vehicle_types.index, y=top_vehicle_types.values, palette="cividis")
plt.title('Top 10 Vehicle Types Involved in crashes', fontsize=16)
plt.xlabel('Vehicle Type', fontsize=14)
plt.ylabel('Number of crashes', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Aggregating data - Complete for Cyclist and Motorist
types_of_crashes = {
    'Pedestrian Injuries': data['NUMBER OF PEDESTRIANS INJURED'].sum(),
    'Cyclist Injuries': data['NUMBER OF CYCLIST INJURED'].sum(),
    'Motorist Injuries': data['NUMBER OF MOTORIST INJURED'].sum(),
    'Pedestrian Deaths': data['NUMBER OF PEDESTRIANS KILLED'].sum(),
    'Cyclist Deaths': data['NUMBER OF CYCLIST KILLED'].sum(),
    'Motorist Deaths': data['NUMBER OF MOTORIST KILLED'].sum()
}

# Converting to DataFrame for easier plotting - we want the items in the dictionary, use the items function
crash_types_df = pd.DataFrame(list(types_of_crashes.items()), columns=['crash Type', 'Count'])

# Plot
plt.figure(figsize=(12, 7))
sns.barplot(x='Count', y='crash Type', data=crash_types_df, palette="mako")
plt.title('Types of crashes and Their Frequencies')
plt.xlabel('Count')
plt.ylabel('Type of crash')
plt.tight_layout()
plt.show()

# Time Series Analysis
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Convert 'CRASH DATE' and 'CRASH TIME' to datetime
data['CRASH DATE'] = pd.to_datetime(data['CRASH DATE'])
data['CRASH TIME'] = pd.to_datetime(data['CRASH TIME'], format='%H:%M')

# Time of Day Analysis
data['Hour of Day'] = data['CRASH TIME'].dt.hour

# Group by 'Hour of Day' and calculate the average number of crashes per hour
average_crashes_per_hour = data.groupby('Hour of Day').size() / data['Hour of Day'].nunique()

# Plot the average number of crashes
plt.figure(figsize=(12, 6))
sns.barplot(x=average_crashes_per_hour.index, y=average_crashes_per_hour.values)
plt.title('Average Number of crashes per Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Average Number of crashes')
plt.xticks(range(0, 24))
plt.show()

# Convert 'CRASH DATE' to datetime format
data['CRASH DATE'] = pd.to_datetime(data['CRASH DATE'])

# Group by month and year to get the number of crashes per month
monthly_crashes = data.groupby(data['CRASH DATE'].dt.to_period("M")).size()

# Plotting the trend over time
plt.figure(figsize=(15, 7))
monthly_crashes.plot()
plt.title('Number of Crashes per Month', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Crashes', fontsize=14)
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

# Count the number of crashes per day, group by CRASH DATE
daily_crashes = data.groupby('CRASH DATE').size()

# Set plot style
sns.set(style="darkgrid")

# Plot the daily crashes time series
plt.figure(figsize=(15, 6))
plt.plot(daily_crashes, label='Daily crashes')
plt.title('Daily Motor Vehicle Collisions in NYC')
plt.xlabel('Date')
plt.ylabel('Number of Crashes')
plt.legend()
plt.show()

# Decompose the time series
decomposition = seasonal_decompose(daily_crashes, model='additive', period=365)

# Plot the decomposed components
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))
decomposition.trend.plot(ax=ax1)
ax1.set_title('Trend')
decomposition.seasonal.plot(ax=ax2)
ax2.set_title('Seasonal')
decomposition.resid.plot(ax=ax3)
ax3.set_title('Residuals')
plt.tight_layout()
plt.show()
# Set style
sns.set_style("whitegrid")

# Plotting the distribution of crashes by borough
plt.figure(figsize=(12, 7))
# Find the count of unique values of BOROUGHS. Hint: Use value_count function.
borough_count = data['BOROUGH'].value_counts()
sns.barplot(x=borough_count.index, y=borough_count.values, palette="viridis")
plt.title('Distribution of Crashes by Borough', fontsize=16)
plt.xlabel('Borough', fontsize=14)
plt.ylabel('Number of Crashes', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

from folium.plugins import HeatMap

# Drop rows with missing latitude and longitude values
data_geo = data.dropna(subset=['LATITUDE', 'LONGITUDE'])

# Create a base map
m = folium.Map(location=[40.730610, -73.935242], zoom_start=10)  # Centered around NYC

# Create a heatmap
heat_data = [[row['LATITUDE'], row['LONGITUDE']] for index, row in data_geo.iterrows()]
HeatMap(heat_data, radius=8, max_zoom=13).add_to(m)

m.save("Heatmap.html")

# Sample a subset of the data for visualization
sample_data_severity = data_geo.sample(n=1000, random_state=42)

# Create a base map
m_severity = folium.Map(location=[40.730610, -73.935242], zoom_start=10)

# Add crashes to the map with color coding and shape coding based on severity
for index, row in sample_data_severity.iterrows():
    if row['NUMBER OF PERSONS KILLED'] > 0:
        color = "red"  # Fatalities

        folium.features.RegularPolygonMarker(
          location=[row['LATITUDE'], row['LONGITUDE']],
          number_of_sides=3,
          radius=5,
          gradient = False,
          color=color,
          fill=True,
          fill_color=color
        ).add_to(m_severity)


    elif row['NUMBER OF PERSONS INJURED'] > 0:
        color = "yellow"  # Injuries
        folium.CircleMarker(
          location=[row['LATITUDE'], row['LONGITUDE']],
          radius=5,
          color=color,
          fill=True,
          fill_color=color
       ).add_to(m_severity)
    else:
        color = "green"  # No injuries or fatalities
        folium.features.RegularPolygonMarker(
          location=[row['LATITUDE'], row['LONGITUDE']],
          number_of_sides=4,
          radius=5,
          gradient = False,
          color=color,
          fill=True,
          fill_color=color
        ).add_to(m_severity)


m_severity.save("severity.html")

import pandas as pd
import folium
from geopy.distance import geodesic
# Load the data (update this to the path where your dataset is located)
data_geo = pd.read_csv("/content/drive/MyDrive/Motor_Vehicle_Collisions_-_Crashes_20250113.csv")
# Ensure the data doesn't have missing or invalid latitude/longitude
data_geo = data_geo.dropna(subset=['LATITUDE', 'LONGITUDE'])
# Optionally: Convert latitude and longitude to numeric values (if they are not already)
data_geo['LATITUDE'] = pd.to_numeric(data_geo['LATITUDE'], errors='coerce')
data_geo['LONGITUDE'] = pd.to_numeric(data_geo['LONGITUDE'], errors='coerce')
# Remove any rows where latitude or longitude could not be converted to a number
data_geo = data_geo.dropna(subset=['LATITUDE', 'LONGITUDE'])
# Sample a subset of the data for visualization
sample_data_severity = data_geo.sample(n=20000, random_state=42)
# Define the approximate location of the Queensboro Bridge entrance
queensboro_bridge_coords = [40.7510, -73.9570]
# Filter data for crashes near the Queensboro Bridge (e.g., within 1 km radius)
def is_near_queensboro(row, center_coords=queensboro_bridge_coords, radius_km=1.0):
    crash_coords = [row['LATITUDE'], row['LONGITUDE']]
    distance = geodesic(crash_coords, center_coords).km
    return distance <= radius_km
# Apply filter to the sampled data
near_queensboro_data = sample_data_severity[sample_data_severity.apply(is_near_queensboro, axis=1)]
# Create a map centered on the Queensboro Bridge
m_severity = folium.Map(location=queensboro_bridge_coords, zoom_start=14)
# Add crashes to the map with color coding and shape coding based on severity
for index, row in near_queensboro_data.iterrows():
    if row['NUMBER OF PERSONS KILLED'] > 0:  # Fatalities
        color = "red"
        folium.features.RegularPolygonMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            number_of_sides=3,  # Red triangle for fatalities
            radius=5,
            gradient=False,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m_severity)
    elif row['NUMBER OF PERSONS INJURED'] > 0:  # Injuries
        color = "orange"
        folium.CircleMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            radius=5,  # Orange circle for injuries
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m_severity)
    else:  # No injuries or fatalities
        color = "blue"
        folium.features.RegularPolygonMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            number_of_sides=4,  # Blue square for no injuries or fatalities
            radius=5,
            gradient=False,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m_severity)
# Save the map
m_severity.save("severity_near_queensboro_bridge.html")

import pandas as pd
import matplotlib.pyplot as plt
from geopy.distance import geodesic

data['CRASH DATE'] = pd.to_datetime(data['CRASH DATE'])
filtered_data = data[(data['CRASH DATE'] >= '2013-01-01') & (data['CRASH DATE'] <= '2015-12-31')]
flushing_coordinates = [40.7684, -73.8327]

def is_within_2km_of_flushing(row, center_coords=flushing_coordinates, radius_km=2.0):
    crash_coords = [row['LATITUDE'], row['LONGITUDE']]
    distance = geodesic(crash_coords, center_coords).km
    return distance <= radius_km

filtered_data = filtered_data.dropna(subset=['LATITUDE', 'LONGITUDE'])
flushing_crashes = filtered_data[filtered_data.apply(is_within_2km_of_flushing, axis=1)]
monthly_crashes = flushing_crashes.groupby(flushing_crashes['CRASH DATE'].dt.to_period("M")).size()

plt.figure(figsize=(15, 7))
monthly_crashes.plot()
plt.title('Number of Crashes per Month Near Flushing (2013-2016)', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Crashes', fontsize=14)
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from geopy.distance import geodesic

data['CRASH DATE'] = pd.to_datetime(data['CRASH DATE'])
flushing_coords = [40.760011, -73.828332]
queensboro_bridge_coords = [40.7510, -73.9570]

def is_within_radius(row, center_coords, radius_km=1):
    crash_coords = [row['LATITUDE'], row['LONGITUDE']]
    distance = geodesic(crash_coords, center_coords).km
    return distance <= radius_km

data = data.dropna(subset=['LATITUDE', 'LONGITUDE'])
flushing_crashes = data[data.apply(is_within_radius, axis=1, center_coords=flushing_coords)]
queensboro_crashes = data[data.apply(is_within_radius, axis=1, center_coords=queensboro_bridge_coords)]

crash_counts = {
    'Flushing': flushing_crashes.shape[0],
    'Queensboro Bridge': queensboro_crashes.shape[0]
}

crash_counts_df = pd.DataFrame(list(crash_counts.items()), columns=['Location', 'Number of Collisions'])
plt.figure(figsize=(8, 5))
plt.bar(crash_counts_df['Location'], crash_counts_df['Number of Collisions'], color=['blue', 'orange'], alpha=0.8)
plt.title('Number of Collisions (1 km Radius)', fontsize=16)
plt.xlabel('Location', fontsize=14)
plt.ylabel('Number of Collisions', fontsize=14)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()



