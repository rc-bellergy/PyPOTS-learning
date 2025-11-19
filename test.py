import pandas as pd
from getTelemetry import get_telemetry_data
import os
from dotenv import load_dotenv

load_dotenv()

def test_telemetry_to_dataframe():
    """
    測試 get_telemetry_data 函數並將返回的 JSON 轉換為 Pandas DataFrame。
    """
    # 從環境變數獲取實體 ID 和授權令牌
    entity_id = os.getenv("TEST_ENTITY_ID", "b57357f0-0934-11f0-ba3c-6989ae50b774")
    authorization_token = os.getenv("AUTHORIZATION_TOKEN")

    if not authorization_token:
        print("錯誤: AUTHORIZATION_TOKEN 未設定在 .env 文件中。")
        return

    print(f"正在使用 Entity ID: {entity_id}")

    # 呼叫 get_telemetry_data 函數
    telemetry_data = get_telemetry_data(
        entityId=entity_id,
        keys="ActiveEnergy_kWh,CurrentA_A,CurrentB_A,CurrentC_A",
        limit=10, # 限制為 10 筆資料以便測試
        agg="AVG" # 範例聚合類型
    )

    if telemetry_data:
        print("成功獲取遙測資料。")
        # 將 JSON 資料轉換為 Pandas DataFrame
        all_dfs = []
        for key, values in telemetry_data.items():
            if values:
                df = pd.DataFrame(values)
                df['ts'] = pd.to_datetime(df['ts'], unit='ms') # 將時間戳轉換為日期時間
                df = df.rename(columns={'value': key}) # 將 'value' 列重命名為鍵名
                df = df.set_index('ts')
                all_dfs.append(df)
        
        if not all_dfs:
            print("沒有遙測資料可以轉換。")
            return None

        # 確保列的順序正確
        desired_columns = ["ActiveEnergy_kWh", "CurrentA_A", "CurrentB_A", "CurrentC_A"]
        
        # 合併所有 DataFrame
        # 將所有 DataFrame 合併，保留所有時間戳
        combined_df = pd.concat(all_dfs, axis=1)

        # 將索引重置為列，方便後續操作
        combined_df = combined_df.reset_index()

        # 將 'ts' 列轉換為 'YYYY-MM-DD HH:MM' 格式，以便按分鐘分組
        combined_df['minute_group'] = combined_df['ts'].dt.strftime('%Y-%m-%d %H:%M')

        # 按 'minute_group' 分組並聚合數據，填補 NaN
        # 使用 transform 來獨立處理每個組，並在原始 DataFrame 上應用 ffill 和 bfill
        for col in desired_columns:
            if col in combined_df.columns:
                combined_df[col] = combined_df.groupby('minute_group')[col].transform(lambda x: x.ffill().bfill())

        # 刪除重複的行，只保留每個 'minute_group' 的第一行（因為數據已經填補）
        final_df = combined_df.drop_duplicates(subset=['minute_group']).copy()
        
        # 清理和最終化 DataFrame
        final_df = final_df.drop(columns=['minute_group'], errors='ignore')
        final_df = final_df.set_index('ts') # 將 'ts' 重新設為索引
        
        existing_columns = [col for col in desired_columns if col in final_df.columns]
        final_df = final_df[existing_columns]

        print("\n合併後的 DataFrame:")
        print(final_df.head())
        print(final_df.info())

        return final_df
    else:
        print("未能獲取遙測資料。")
        return None

if __name__ == "__main__":
    dataframes = test_telemetry_to_dataframe()
    if dataframes is not None and not dataframes.empty:
        print("\n遙測資料已成功轉換為 Pandas DataFrame。")