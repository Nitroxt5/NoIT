import pandas as pd


def count_max_decimal_places(col: pd.Series):
    if not pd.api.types.is_float_dtype(col.dtype):
        raise TypeError(f'Can`t count decimal places in column with `{col.dtype}` `type')
    tmp_col = col.astype(str)
    return tmp_col.str.split('.', n=1).str[-1].str.len().max()
