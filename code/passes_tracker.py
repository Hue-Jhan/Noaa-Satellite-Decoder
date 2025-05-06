import json
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pyorbital.orbital import Orbital
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pytz
import random
import warnings

# remove warning related to timezone handling in pyorbital
warnings.filterwarnings("ignore", message="no explicit representation of timezones available for np.datetime64")


def load_dataset_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


dataset_files = ["dataset.json", "dataset2.json", "dataset4.json"]  # Add your file names here
satellite_colors = {
    "NOAA-18": 'red',
    "NOAA-19": 'blue',
    "NOAA-15": 'green',
    "MetOp-A": 'orange',
    "MetOp-B": 'purple',
    "MetOp-C": 'cyan',
    "JPSS-1": 'magenta'
}


def get_satellite_color(satellite_name):
    if satellite_name in satellite_colors:
        return satellite_colors[satellite_name]
    else:
        return random.choice(['yellow', 'brown', 'pink', 'lime', 'teal'])


fig = plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_global()
ax.stock_img()
ax.coastlines()
ax.gridlines(draw_labels=True)

for dataset_file in dataset_files:
    try:
        dataset = load_dataset_json(dataset_file)

        satellite_name = dataset.get("satellite", "Unknown Satellite")
        timestamp = dataset.get("timestamp", None)
        if not timestamp:
            print(f"Warning: No timestamp in {dataset_file}")
            continue

        timezone_str = dataset.get("timezone", "UTC")
        timezone_obj = pytz.timezone(timezone_str)
        dt = datetime.fromtimestamp(timestamp, timezone.utc)
        dt = dt.astimezone(timezone_obj)
        sat = Orbital(satellite_name)
        utc_time = dt.astimezone(pytz.utc)
        lon, lat, alt = sat.get_lonlatalt(utc_time)
        color = get_satellite_color(satellite_name)
        ax.plot(lon, lat, 'o', markersize=4, color=color,
                label=f"{satellite_name} @ {dt.strftime('%Y-%m-%d %H:%M:%S')}")

        # print(f"{satellite_name} pass at {dt}: Lat={lat:.2f}, Lon={lon:.2f}, Alt={alt:.1f} km")

    except Exception as e:
        print(f"Error processing {dataset_file}: {e}")

plt.title("Satellite Passes and Trajectories")
plt.legend()
plt.savefig('satellite_trajectory_overlay.png', dpi=200)
plt.show()
