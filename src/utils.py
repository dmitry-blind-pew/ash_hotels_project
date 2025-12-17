from datetime import date

from fastapi import HTTPException


def check_date_from_and_date_to(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(status_code=422, detail="Дата заезда позже даты выезда")