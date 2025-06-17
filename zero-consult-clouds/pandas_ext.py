"""Custom Extension"""

from __future__ import annotations

from typing import List

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype


@pd.api.extensions.register_dataframe_accessor("zero-consult-clouds")
class ZeroAccessor:
    """Provide helper methods for :class:`pandas.DataFrame`."""

    def __init__(self, pandas_obj: pd.DataFrame) -> None:
        self._obj = pandas_obj

    def func(self, x):
        print(x)

