import pandas as pd
import numpy as np
import os
import getTelemetry

def read_power_usage_data(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return None
    
    try:
        df = pd.read_csv(filepath, sep=';', parse_dates=['Timestamp'])
        df.set_index('Timestamp', inplace=True)
        print("Successfully read data:")
        print(df.head()) # Print first 5 rows to verify
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def resample_power_data(df, rule='1h'):
    print(f"\nResampling data to {rule} frequency...")
    # Select only the numeric column 'Total_Power_Usage_17/F' for resampling
    resampled_df = df['Total_Power_Usage_17/F'].resample(rule).mean().to_frame()
    # print("Resampled data head:")
    # print(resampled_df.head())
    return resampled_df

def save_data_to_csv(df, output_filepath):
    print(f"\nSaving data to {output_filepath}...")
    output_dir = os.path.dirname(output_filepath)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        df.to_csv(output_filepath)
        # print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

def create_sliding_windows(data, window_len):
    """
    將 2D 數據 (Time, Features) 轉換為 3D (Samples, Window, Features)
    """
    n_steps = len(data)
    n_features = data.shape[1]
    
    # 計算可以切出多少個樣本
    # 如果數據長度是 100，窗口是 96，我們只能切出 (100 - 96 + 1) = 5 個樣本
    n_samples = n_steps - window_len + 1
    
    if n_samples <= 0:
        raise ValueError("數據長度小於窗口長度，無法切分！")
    
    # 初始化 3D 陣列
    X = np.zeros((n_samples, window_len, n_features))
    
    # 填入數據 (這裡使用最簡單的迴圈，Numpy 有更進階的 stride_tricks 但較難懂)
    for i in range(n_samples):
        X[i] = data[i : i + window_len]
        
    return X

if __name__ == "__main__":
    csv_filepath = 'data/total-power-usage-17F.csv'
    power_data = read_power_usage_data(csv_filepath)
    

    if power_data is not None:
        print("*" * 30)
        print(f"\nOriginal data total rows: {len(power_data)}")
        
        # Resample the data to 1 hour frequency
        resampled_power_data = resample_power_data(power_data, rule='1h')
        print(f"\nResampled data total rows: {len(resampled_power_data)}")
        
        # Define output path and save the resampled data
        output_filepath = 'data/output/resampled_power_usage.csv'
        save_data_to_csv(resampled_power_data, output_filepath)

        # Display sample rows to show the effect of resampling
        # print("\n--- Comparing Original and Resampled Data (Sample) ---")
        
        # Get a time range for comparison
        # start_time = power_data.index.min()
        # end_time = power_data.index.min() + pd.Timedelta(hours=5) # Adjust range as needed

        # print("\nOriginal Data Sample:")
        # print(power_data.loc[start_time:end_time])

        # print("\nResampled Data Sample:")
        # print(resampled_power_data.loc[start_time:end_time])

        # Create sliding windows from the resampled data
        WINDOW_LEN = 24*7  # 7 days of hourly data
        X_intact = create_sliding_windows(resampled_power_data.values, WINDOW_LEN)
        print("-" * 30)
        print(f"最終 PyPOTS 輸入格式 (X): {X_intact.shape}")
        print("(樣本數, 時間步長, 特徵數)")