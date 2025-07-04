import pandas as pd


# def split_to_data_and_target(data: pd.DataFrame):
#     col_list = ''
#     possible_choices = []
#     for i, col in enumerate(data.columns, start=1):
#         col_list += f'{i}. {col}\n'
#         possible_choices.append(f'{i}')
#     choice = get_choice(f'Select which column is a target:\n{col_list}', tuple(possible_choices))
#     target_col = data.columns[int(choice) - 1]
#     target = data[target_col]
#     data = data.drop(target_col, axis=1)
#     return data, target


def count_max_decimal_places(col: pd.Series):
    if not pd.api.types.is_float_dtype(col.dtype):
        raise TypeError(f'Can`t count decimal places in column with `{col.dtype}` `type')
    tmp_col = col.astype(str)
    return tmp_col.str.split('.', n=1).str[-1].str.len().max()
