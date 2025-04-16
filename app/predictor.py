import json
import pandas as pd
import joblib

MAX_LEN = 74  # keys go from _0 through _73
model = joblib.load('app/ml_model/posture_classifier.pkl')
def parse_json_string(raw: str) -> dict:
    """
    Turn a string that looks like JSON-but-has [...] around the
    key/value pairs into a real dict.
    """
    s = raw.strip()
    if s.startswith('[') and s.endswith(']'):
        s = '{' + s[1:-1] + '}'
    return json.loads(s)


def normalize_length(arr: list, length: int = MAX_LEN) -> list:
    """
    Truncate or pad with zeros so that `arr` has exactly `length` elements.
    """
    if len(arr) >= length:
        return arr[:length]
    else:
        return arr + [0.0] * (length - len(arr))


def dict_to_instance(d: dict) -> pd.DataFrame:
    """
    Given a dict whose values are lists (e.g. "roll0": [...], ...),
    normalize each to MAX_LEN, then flatten to a single-row DataFrame
    with columns key_0, key_1, ..., key_73.
    """
    flat = {}
    for key, arr in d.items():
        arr = normalize_length(arr, MAX_LEN)
        for i, v in enumerate(arr):
            flat[f"{key}_{i}"] = v

    df = pd.DataFrame([flat])
    df = df.loc[:, ~df.columns.str.startswith("env")]

    # Drop any unwanted columns (e.g. rep_id) if present
    if 'rep_id' in df.columns:
        df.drop(columns=['rep_id'], inplace=True)

    return df


def predict_posture(input_data: str):
    """
    :param input_data: raw string that looks like JSON
    :return: model prediction
    """
    # 1) parse into a dict
    try:
        d = parse_json_string(input_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not parse input_data as JSON: {e}")

    # 2) normalize & flatten to one‑row DataFrame
    df = dict_to_instance(d)

    # 3) (optional) re‑index columns to your exact training order:
    # feature_order = [ f"{k}_{i}" for k in [...] for i in range(MAX_LEN) ]
    # df = df.reindex(columns=feature_order, fill_value=0.0)

    # 4) feed to your model
    y_pred = model.predict(df.values)   # or df.iloc[0] depending on your model API
    
    y_pred = y_pred[0]  # if you want a single value instead of an array

    print(y_pred)
    
    return True if y_pred == "good" else False
