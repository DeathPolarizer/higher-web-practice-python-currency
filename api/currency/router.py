from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.deps import get_currency_service, get_current_user
from core.exceptions import CurrencyNotFoundError
from domain.currency.dto import CurrencyDTO, ExchangeRateDTO
from domain.currency.service import CurrencyService
from domain.users.models import User

router = APIRouter(prefix="/currencies", tags=["currencies"])
CurrentUserDep = Annotated[User, Depends(get_current_user)]
CurrencyServiceDep = Annotated[CurrencyService, Depends(get_currency_service)]


@router.get("", response_model=list[CurrencyDTO])
async def list_currencies(
    current_user: CurrentUserDep,
    service: CurrencyServiceDep,
):
    return await service.list_currencies()


@router.get(
    "/{currency_code}/history",
    summary="История курса валюты",
    response_model=list[ExchangeRateDTO],
)
async def get_currency_history(
    currency_code: str,
    current_user: CurrentUserDep,
    service: CurrencyServiceDep,
    start_date: Annotated[date, Query(description="(YYYY-MM-DD)")],
    end_date: Annotated[date, Query(description="(YYYY-MM-DD)")],
):
    try:
        return await service.get_rate_history(
            currency_code, start_date, end_date
        )
    except CurrencyNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Currency not found",
        )


@router.get(
    "/{currency_code}/all",
    summary="Все курсы валют",
    response_model=list[ExchangeRateDTO],
)
async def get_all_currency_rates(
    currency_code: str,
    current_user: CurrentUserDep,
    service: CurrencyServiceDep,
):
    try:
        return await service.get_rates_for_currency(currency_code)
    except CurrencyNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Currency not found",
        )


@router.get(
    "/{currency_code}",
    summary="Последний курс",
    response_model=ExchangeRateDTO,
)
async def get_latest_currency_rate(
    currency_code: str,
    current_user: CurrentUserDep,
    service: CurrencyServiceDep,
):
    try:
        return await service.get_latest_rate(currency_code)
    except CurrencyNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Currency not found",
        )
