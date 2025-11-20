import requests
import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()

def get_telemetry_data(
    entityType: str = "DEVICE",
    entityId: str = "b57357f0-0934-11f0-ba3c-6989ae50b774",
    keys: str = "ActiveEnergy_kWh",
    limit: int = 1000,
    startTs: int = None,
    endTs: int = None,
    intervalType: str = None,
    interval: int = 0,
    timeZone: str = "Asia/Hong_Kong",
    agg: str = None,
    orderBy: str = "ASC",
    useStrictDataTypes: bool = False,
    authorization_token: str = os.getenv("AUTHORIZATION_TOKEN")
):
    """
    Fetch telemetry data from ThingsBoard API.

    Args:
        entityType (str): Entity type, e.g., "DEVICE".
        entityId (str): Entity ID.
        keys (str): Telemetry keys to fetch, comma-separated.
        limit (int): Limit on the number of data points to return.
        startTs (int): Start timestamp (Unix, milliseconds). If None, defaults to 7 days ago.
        endTs (int): End timestamp (Unix, milliseconds). If None, defaults to now.
        intervalType (str): Time interval type for aggregation (e.g., "HOUR", "DAY").
        interval (int): Time interval value for aggregation.
        timeZone (str): Time zone (e.g., "Asia/Hong_Kong").
        agg (str): Aggregation type (e.g., "NONE", "AVG", "SUM").
        orderBy (str): Sorting order (e.g., "ASC", "DESC").
        useStrictDataTypes (bool): Whether to use strict data types.
        authorization_token (str): Bearer token for API requests.

    Returns:
        dict: JSON response containing telemetry data, or None if request fails.
    """
    base_url = "https://ioter.mpiot.com.hk/api/plugins/telemetry"
    endpoint = f"{base_url}/{entityType}/{entityId}/values/timeseries"

    # Calculate default timestamps (in milliseconds)
    if endTs is None:
        endTs = int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)
    if startTs is None:
        startTs = int((datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)).timestamp() * 1000)

    params = {
        "keys": keys,
        "startTs": startTs,
        "endTs": endTs,
        "limit": limit,
        "timeZone": timeZone,
        "orderBy": orderBy,
        "useStrictDataTypes": useStrictDataTypes
    }
    if intervalType is not None:
        params["intervalType"] = intervalType
    if interval is not None:
        params["interval"] = interval
    if agg is not None:
        params["agg"] = agg

    # Add request headers
    headers = {
        "accept": "application/json",
        "X-Authorization": f"Bearer {authorization_token}"
    }

    try:
        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()  # Raises HTTPError if the request was unsuccessful
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching telemetry data: {e}")
        return None

# # Example usage (optional, for testing)
if __name__ == "__main__":
    data = get_telemetry_data()
    if data:
        print("Telemetry Data:")
        for key, values in data.items():
            print(f"  {key}:")
            for entry in values:
                print(f"    Timestamp: {entry['ts']}, Value: {entry['value']}")
    else:
        print("Failed to retrieve telemetry data.")