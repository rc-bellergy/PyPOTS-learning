import pandas as pd
from getTelemetry import get_telemetry_data
from auth import get_jwt_token
import os
from dotenv import load_dotenv

load_dotenv()

def test_telemetry_to_dataframe():
    """
    Test the get_telemetry_data function and convert the returned JSON to Pandas DataFrame.
    """
    # Get entity ID, username and password from environment variables
    entity_id = os.getenv("TEST_ENTITY_ID", "b57357f0-0934-11f0-ba3c-6989ae50b774")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    if not username or not password:
        print("Error: USERNAME or PASSWORD is not set in .env file.")
        return

    print(f"Using Entity ID: {entity_id}")

    # Get JWT token using username and password
    try:
        print("Getting JWT token...")
        token_data = get_jwt_token(username=username, password=password)
        authorization_token = token_data.get('token')
        
        if not authorization_token:
            print("Error: Failed to get authorization token")
            return
            
        print("Successfully obtained JWT token")
        
    except Exception as e:
        print(f"Error getting JWT token: {e}")
        return

    # Call get_telemetry_data function with the obtained token
    telemetry_data = get_telemetry_data(
        entityId=entity_id,
        keys="ActiveEnergy_kWh,CurrentA_A,CurrentB_A,CurrentC_A",
        limit=10, # Limit to 10 records for testing
        agg="AVG", # Example aggregation type
        authorization_token=authorization_token
    )

    if telemetry_data:
        print("Successfully retrieved telemetry data.")
        # Convert JSON data to Pandas DataFrame
        all_dfs = []
        for key, values in telemetry_data.items():
            if values:
                df = pd.DataFrame(values)
                df['ts'] = pd.to_datetime(df['ts'], unit='ms') # Convert timestamp to datetime
                df = df.rename(columns={'value': key}) # Rename 'value' column to key name
                df = df.set_index('ts')
                all_dfs.append(df)
        
        if not all_dfs:
            print("No telemetry data to convert.")
            return None

        # Ensure correct column order
        desired_columns = ["ActiveEnergy_kWh", "CurrentA_A", "CurrentB_A", "CurrentC_A"]
        
        # Merge all DataFrames
        # Combine all DataFrames, preserving all timestamps
        combined_df = pd.concat(all_dfs, axis=1)

        # Reset index to column for easier operations
        combined_df = combined_df.reset_index()

        # Convert 'ts' column to 'YYYY-MM-DD HH:MM' format for minute grouping
        combined_df['minute_group'] = combined_df['ts'].dt.strftime('%Y-%m-%d %H:%M')

        # Group by 'minute_group' and aggregate data, filling NaN values
        # Use transform to process each group independently and apply ffill and bfill on the original DataFrame
        for col in desired_columns:
            if col in combined_df.columns:
                combined_df[col] = combined_df.groupby('minute_group')[col].transform(lambda x: x.ffill().bfill())

        # Remove duplicate rows, keeping only the first row for each 'minute_group' (since data has been filled)
        final_df = combined_df.drop_duplicates(subset=['minute_group']).copy()
        
        # Clean and finalize DataFrame
        final_df = final_df.drop(columns=['minute_group'], errors='ignore')
        final_df = final_df.set_index('ts') # Reset 'ts' as index
        
        existing_columns = [col for col in desired_columns if col in final_df.columns]
        final_df = final_df[existing_columns]

        print("\nMerged DataFrame:")
        print(final_df.head())
        # print(final_df.info())

        return final_df
    else:
        print("Failed to retrieve telemetry data.")
        return None

if __name__ == "__main__":
    dataframes = test_telemetry_to_dataframe()
    if dataframes is not None and not dataframes.empty:
        print("\nTelemetry data successfully converted to Pandas DataFrame.")