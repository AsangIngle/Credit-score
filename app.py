import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans

def process_json(uploaded_file):
    try:
        raw_data = json.load(uploaded_file)
        df = pd.json_normalize(raw_data)
    except Exception:
        return None, "Invalid JSON file"

    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
        df.fillna(0, inplace=True)
    except Exception:
        return None, "Failed during timestamp conversion or NaN handling"

    label_cols = ['network', 'protocol', 'action', 
                  'actionData.assetSymbol', 
                  'actionData.collateralReserveSymbol',
                  'actionData.principalReserveSymbol',
                  'actionData.borrowRateMode']

    for col in label_cols:
        if col in df.columns and (df[col].dtype == 'object' or df[col].dtype == np.dtype('O')):
            try:
                df[col] = LabelEncoder().fit_transform(df[col].astype(str))
            except:
                continue

    try:
        agg_df = df.groupby("userWallet").agg({
            "action": "nunique",
            "blockNumber": "count",
            "actionData.amount": "sum",
            "actionData.collateralAmount": "sum",
            "actionData.assetPriceUSD": "mean",
            "network": "nunique",
            "protocol": "nunique",
            "actionData.borrowRate": "mean",
            "actionData.variableTokenDebt": "sum",
            "actionData.stableTokenDebt": "sum",
        }).rename(columns={
            "action": "num_unique_actions",
            "blockNumber": "num_transactions",
            "actionData.amount": "total_amount",
            "actionData.collateralAmount": "total_collateral",
            "actionData.assetPriceUSD": "avg_asset_price",
            "network": "num_networks",
            "protocol": "num_protocols",
            "actionData.borrowRate": "avg_borrow_rate",
            "actionData.variableTokenDebt": "total_variable_debt",
            "actionData.stableTokenDebt": "total_stable_debt"
        }).reset_index()
    except Exception:
        return None, "Failed during aggregation"

    try:
        features = agg_df.drop(columns=["userWallet"])
        kmeans = KMeans(n_clusters=5, random_state=42)
        agg_df['cluster'] = kmeans.fit_predict(features)
    except Exception:
        return None, "KMeans clustering failed"

    try:
        cluster_to_score = {
            0: 200,
            1: 400,
            2: 600,
            3: 800,
            4: 1000
        }
        agg_df['credit_score'] = agg_df['cluster'].map(cluster_to_score)
    except Exception:
        return None, "Failed to assign scores"

    return agg_df, None
