import pandas as pd
import numpy as np
import os
import glob
import json

def load_openaq(path: str = "data/station_data_2025") -> pd.DataFrame:
    """Read partitioned sensor data and preprocess into wide table.
    
    This replicates the transformation used by the dashboard so that
    standalone scripts can operate on the same cleaned dataset.
    """
    
    # Base directory for the partitioned data
    base_dir = path
    
    # Load zone mapping to assign Industrial/Residential labels
    json_path = "data/accepted_stations.json"
    zone_map = {}
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            zone_map = json.load(f)
            
    dfs = []
    # Loop over station directories
    station_dirs = glob.glob(os.path.join(base_dir, "station=*"))
    
    params = ["pm25", "pm10", "no2", "ozone", "temperature", "humidity"]
    
    for s_dir in station_dirs:
        station_id = os.path.basename(s_dir).split("=")[1]
        
        s_data = {}
        for p in params:
            fpath = os.path.join(s_dir, f"{p}.csv")
            if os.path.exists(fpath):
                try:
                    # Read single column value file
                    s_data[p] = pd.read_csv(fpath, header=None).iloc[:, 0].values
                except Exception:
                    s_data[p] = []
                
        if len(s_data) != 6:
            # Skip stations without all 6 parameters
            continue
            
        # Truncate to minimum length across all 6 parameters
        min_len = min(len(arr) for arr in s_data.values())
        if min_len == 0:
            continue
            
        s_data_trunc = {k: v[:min_len] for k, v in s_data.items()}
        st_df = pd.DataFrame(s_data_trunc)
        st_df["station"] = f"Station_{station_id}" # Maintain old dashboard format or use raw ID
        st_df["zone"] = zone_map.get(str(station_id), "Residential")
        
        # Reconstruct hourly timeline starting Jan 1, 2025
        st_df["datetime"] = pd.date_range(start="2025-01-01 00:00:00", periods=len(st_df), freq="h")
        
        dfs.append(st_df)
        
    if not dfs:
        return pd.DataFrame()
        
    df = pd.concat(dfs, ignore_index=True)
    df["hour"] = df["datetime"].dt.hour
    df["day"] = df["datetime"].dt.day
    df["month"] = df["datetime"].dt.month
    
    # --- SANITIZATION BOUNDARY ---
    # Remove physically impossible and obviously corrupted sensor readings
    df = df[(df['pm25'] >= 0) & (df['pm25'] <= 5000)]
    df = df[(df['pm10'] >= 0) & (df['pm10'] <= 5000)]
    df = df[(df['no2'] >= 0) & (df['no2'] <= 2000)]
    df = df[(df['ozone'] >= 0) & (df['ozone'] <= 2000)]
    df = df[(df['temperature'] >= -50) & (df['temperature'] <= 70)]
    df = df[(df['humidity'] >= 0) & (df['humidity'] <= 100)]
    
    return df

