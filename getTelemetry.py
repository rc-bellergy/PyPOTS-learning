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
    從 ThingsBoard API 獲取遙測資料。

    Args:
        entityType (str): 實體類型，例如 "DEVICE"。
        entityId (str): 實體 ID。
        keys (str): 要獲取的遙測鍵，以逗號分隔。
        limit (int): 返回的資料點數量限制。
        startTs (int): 開始時間戳記（Unix，毫秒）。如果為 None，則預設為 7 天前。
        endTs (int): 結束時間戳記（Unix，毫秒）。如果為 None，則預設為現在。
        intervalType (str): 聚合的時間間隔類型 (e.g., "HOUR", "DAY").
        interval (int): 聚合的時間間隔值.
        timeZone (str): 時區 (e.g., "Asia/Hong_Kong").
        agg (str): 聚合類型 (e.g., "NONE", "AVG", "SUM").
        orderBy (str): 排序方式 (e.g., "ASC", "DESC").
        useStrictDataTypes (bool): 是否使用嚴格的資料類型。
        authorization_token (str): 用於 API 請求的 Bearer 令牌。

    Returns:
        dict: 包含遙測資料的 JSON 回應，如果請求失敗則為 None。
    """
    base_url = "https://ioter.mpiot.com.hk/api/plugins/telemetry"
    endpoint = f"{base_url}/{entityType}/{entityId}/values/timeseries"

    # 計算預設時間戳記 (以毫秒為單位)
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

    # 新增請求頭
    headers = {
        "accept": "application/json",
        "X-Authorization": f"Bearer {authorization_token}"
    }

    try:
        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()  # 如果請求不成功，將引發 HTTPError
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching telemetry data: {e}")
        return None

# # 範例用法 (可選，用於測試)
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