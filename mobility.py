from pyspainmobility import Mobility, Zones
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

# getting 1 week of mobility data. In this case, we download the data from March 10 to March 16 
mobility_data = Mobility(version=2, zones='lua', start_date='2024-10-14', end_date='2024-10-20')
# and we extract the OD matrices 
mobility_data.get_od_data()


# similarly, we download the zones concerning municipalities using the Zones module
zones = Zones ( zones = 'gau', version=2)
zones = zones.get_zone_geodataframe()

od = pd.read_parquet(r'C:\Users\pmesparza\data\Viajes_GAU_2024-10-14_2024-10-20_v2.parquet')
od = od[(od['id_origin']=='GAU Navarra')]
od = od.groupby(['date','hour'])['n_trips'].sum().reset_index()


# Load the dataset
df = od

# Convert date to datetime and create a unified datetime index
df['date'] = pd.to_datetime(df['date'])
df['datetime'] = df['date'] + pd.to_timedelta(df['hour'], unit='h')

# Sort values by time to ensure chronological order
df = df.sort_values(by='datetime')

# Set the plot style
sns.set(style="whitegrid", palette="muted", font_scale=1.2)

# Plot the time series
plt.figure(figsize=(14, 6))
sns.lineplot(data=df, x='datetime', y='n_trips', marker='o', color='steelblue')

# Customize the plot
plt.title('Mobility Trend From Greater Urban Area of Madrid to Spain (1 Week)', fontsize=16)
plt.xlabel('Date and Time')
plt.ylabel('Number of Trips from Madrid')
plt.xticks(rotation=45)
plt.tight_layout()
# Show the plot
plt.show()