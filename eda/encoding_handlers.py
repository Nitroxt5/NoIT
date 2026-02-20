import pandas as pd

from eda.utils import count_max_decimal_places


def encode_data(data: pd.DataFrame):
    data = data.convert_dtypes()
    columns = data.columns
    for col in columns:
        if data[col].isin([0, 1]).all():
            continue
        if pd.api.types.is_numeric_dtype(data[col].dtype):
            data = _binary_encoding(data, col)
            continue
        data = _one_hot_encoding(data, col)
    return data


def _one_hot_encoding(data: pd.DataFrame, col: str):
    data = _label_encoding(data, col)
    for i, el in data[col].items():
        new_col = f'{col}_{el}'
        if new_col not in data:
            data[new_col] = 0
        data.at[i, new_col] = 1
    data = data.drop(col, axis=1)
    return data


def _binary_encoding(data: pd.DataFrame, col: str):
    data = _label_encoding(data, col)
    bits_to_encode = int(data[col].max() - data[col].min()).bit_length()
    for i in range(bits_to_encode):
        data[col + str(i)] = [(el >> i) & 1 for el in data[col].values]
    data = data.drop(col, axis=1)
    return data


def _label_encoding(data: pd.DataFrame, col: str):
    if pd.api.types.is_numeric_dtype(data[col].dtype):
        if pd.api.types.is_float_dtype(data[col].dtype):
            decimal_places_count = count_max_decimal_places(data[col])
            data[col] *= 10 ** decimal_places_count
            data[col] = data[col].astype('int64')
        low = data[col].min()
        data[col] = data[col].map({value: value - low for value in data[col].unique()})
    else:
        data[col] = data[col].map({value: label for label, value in enumerate(data[col].unique())})
    return data
