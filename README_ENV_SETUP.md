# 環境設定說明

## 概述

此專案已成功整合 `.env` 檔案設定，自動載入 `https://ioter.mpiot.com.hk` 和相關 API 設定。

## 設定檔案

### `.env` 檔案內容
```
BASE_URL="https://ioter.mpiot.com.hk"
AUTHORIZATION_TOKEN="eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJtaWNoYWVsLmNoYXVAbXBpb3QuY29tLmhrIiwidXNlcklkIjoiZTk1Yjc1MzAtZDMwZi0xMWVmLTk1MjctMjcwNTEyYTI5NDM4Iiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJzZXNzaW9uSWQiOiI0MmQzYmNhZS1lMTRhLTQ3ZjItOGJmZS0xODA1YjMzZTQ4Y2IiLCJleHAiOjE3NjM1NTA1OTYsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNzYzNTQxNTk2LCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiMzYxOGEwODAtYTJhMi0xMWVmLWFlMTYtNDc4ZTgzYWQ5ZmE2IiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCJ9.OO2_N_Vd2FaGp62QFpCLu7wrrGCW3RNmRrMwqFrLAuoTFyC-SQiVFOKp-DWqZHRmXtKtqztC6hmrDCiNyqZvsg"
```

## 整合的模組

### 1. config.py
- 集中管理所有環境變數
- 自動載入 `.env` 檔案
- 提供預設值和驗證功能

### 2. auth.py
- 更新為使用 `Config` 類別
- 自動從 `.env` 載入 `BASE_URL`
- 支援自訂 base_url 參數

### 3. getTelemetry.py
- 使用 `Config` 類別載入設定
- 自動使用 `BASE_URL` 和 `AUTHORIZATION_TOKEN`
- 簡化程式碼結構

## 使用方法

### 基本使用（自動載入 .env）
```python
from getTelemetry import get_telemetry_data

# 自動使用 .env 中的 BASE_URL 和 AUTHORIZATION_TOKEN
data = get_telemetry_data()
```

### 使用 AuthManager
```python
from auth import AuthManager

# 自動使用 .env 中的 BASE_URL
auth = AuthManager()
```

### 手動指定 URL（覆寫 .env）
```python
from auth import AuthManager

# 手動指定 base_url（會覆寫 .env 設定）
auth = AuthManager(base_url="https://custom-url.com")
```

## 測試設定

執行測試腳本驗證設定：
```bash
python test_env_config.py
```

## 注意事項

1. **令牌過期**: 目前 `.env` 中的 `AUTHORIZATION_TOKEN` 已過期，需要更新
2. **依賴套件**: 需要安裝 `python-dotenv` 套件來載入 `.env` 檔案
3. **備用方案**: 如果 `.env` 檔案不存在，會使用系統環境變數

## 檔案結構
```
.
├── .env                    # 環境變數設定
├── config.py              # 設定管理類別
├── auth.py                # 認證管理（已整合 .env）
├── getTelemetry.py        # 遙測資料獲取（已整合 .env）
├── test_env_config.py     # 設定測試腳本
└── README_ENV_SETUP.md    # 本說明文件
```

## 下一步

1. 更新 `.env` 檔案中的 `AUTHORIZATION_TOKEN` 為有效的令牌
2. 執行 `test_env_config.py` 確認所有功能正常
3. 開始使用整合後的 API 功能