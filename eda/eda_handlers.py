import numpy as np
import pandas as pd

from eda.utils import get_choice


def handle_unimportant(data: pd.DataFrame):
    data = data.convert_dtypes()
    unique_counts = data.nunique()
    row_count = len(data)
    for col, count in unique_counts.items():
        if pd.api.types.is_float_dtype(data[col].dtype):
            continue
        if count * 2 < row_count:
            continue
        choice = get_choice(f'Column `{col}` seems to be unimportant. Remove? (y/n) ')
        if choice == 'y' or choice == 'yes':
            data.drop(col, axis=1, inplace=True)
            print(f'Column `{col}` removed.')
        else:
            print(f'Column `{col}` was not removed.')
    return data


def handle_duplicates(data: pd.DataFrame):
    duplicates_count = data.duplicated().value_counts().get(True, 0)
    if duplicates_count == 0:
        print('No duplicates found.')
        return data
    choice = get_choice(f'Detected {duplicates_count} duplicates. Remove? (y/n) ')
    if choice == 'y' or choice == 'yes':
        data.drop_duplicates(inplace=True)
        print(f'Removed {duplicates_count} duplicates.')
    else:
        print('Duplicates were not removed.')
    return data


def handle_nulls(data: pd.DataFrame):
    data = data.convert_dtypes()
    nulls_count = data.isnull().sum()
    null_cols_count = (nulls_count > 0).sum()
    if null_cols_count == 0:
        print('No empty values found.')
        return data
    print(f'Detected {null_cols_count} columns with empty values.')
    cols_with_empty_values = data.columns[data.isnull().any()]
    cols_which_rows_to_drop = []
    for col in cols_with_empty_values:
        if pd.api.types.is_numeric_dtype(data[col].dtype):
            choice = get_choice(f'{nulls_count[col]} empty values detected in column `{col}`. '
                                f'How to handle them? (dc-delete column, dr-delete rows, fz-fill with zeros,'
                                f' fa-fill with average, fr-fill with random) ',
                                ('dc', 'dr', 'fz', 'fa', 'fr'))
        else:
            choice = get_choice(f'{nulls_count[col]} empty values detected in column `{col}`. '
                                f'How to handle them? (dc-delete column, dr-delete rows, fr-fill with random) ',
                                ('dc', 'dr', 'fr'))
        if choice == 'dc':
            data.drop(col, axis=1, inplace=True)
            print(f'Column `{col}` removed.')
            continue
        if choice == 'dr':
            cols_which_rows_to_drop.append(col)
            print(f'{nulls_count[col]} rows, containing empty values in column `{col}` removed.')
            continue
        if choice == 'fz':
            data.fillna({col: 0}, inplace=True)
            print(f'{nulls_count[col]} cells, containing empty values in column `{col}` were filled with value 0.')
            continue
        if choice == 'fa':
            avg = data[col].mean()
            if pd.api.types.is_integer_dtype(data[col].dtype):
                avg = round(avg)
            data.fillna({col: avg}, inplace=True)
            print(f'{nulls_count[col]} cells, containing empty values in column `{col}` '
                  f'were filled with average value {avg}.')
            continue
        if choice == 'fr':
            if pd.api.types.is_numeric_dtype(data[col].dtype):
                low = data[col].min()
                high = data[col].max()
                if pd.api.types.is_integer_dtype(data[col].dtype):
                    data[col] = data[col].map(lambda x: np.random.randint(low, high) if pd.isna(x) else x)
                else:
                    data[col] = data[col].map(lambda x: np.random.uniform(low, high) if pd.isna(x) else x)
            else:
                unique_values = data[col].drop_duplicates().dropna()
                data[col] = data[col].map(lambda x: np.random.choice(unique_values) if pd.isna(x) else x)
            print(f'{nulls_count[col]} cells, containing empty values in column `{col}` '
                  f'were filled with random values.')
    data.dropna(subset=cols_which_rows_to_drop, inplace=True)
    data = data.convert_dtypes()
    return data
