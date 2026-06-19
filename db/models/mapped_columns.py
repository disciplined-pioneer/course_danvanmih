import pytz
from datetime import datetime
from typing import Annotated
from sqlalchemy.orm import mapped_column
from sqlalchemy import BigInteger, DateTime, String, text, Float


# Определение столбцов без использования Annotated
intpk = Annotated[
    int,
    mapped_column(primary_key=True, autoincrement=True, init=False)
]