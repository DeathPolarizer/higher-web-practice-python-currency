import datetime
from decimal import Decimal

from sqlalchemy import (
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.constants import (
    CURRENCY_CHAR_CODE_MAX_LEN,
    CURRENCY_NAME_MAX_LEN,
    CURRENCY_NUM_CODE_MAX_LEN,
    EXCHANGE_RATE_PRECISION,
    EXCHANGE_RATE_SCALE,
)
from core.db import Base


class Currency(Base):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    char_code: Mapped[str] = mapped_column(
        String(CURRENCY_CHAR_CODE_MAX_LEN),
        unique=True,
        index=True,
        nullable=False,
    )
    num_code: Mapped[str] = mapped_column(
        String(CURRENCY_NUM_CODE_MAX_LEN), nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(CURRENCY_NAME_MAX_LEN), nullable=False
    )
    nominal: Mapped[int] = mapped_column(Integer, nullable=False)

    rates: Mapped[list["ExchangeRate"]] = relationship(
        "ExchangeRate", back_populates="currency"
    )

    def __repr__(self) -> str:
        return (
            f"Currency id={self.id} "
            f"char_code={self.char_code!r} "
            f"name={self.name!r} "
        )


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    __table_args__ = (
        UniqueConstraint(
            "currency_id",
            "date",
            name="uq_currency_date",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id"),
        nullable=False,
    )
    rate: Mapped[Decimal] = mapped_column(
        Numeric(EXCHANGE_RATE_PRECISION, EXCHANGE_RATE_SCALE),
        nullable=False,
    )
    date: Mapped[datetime.date] = mapped_column(
        Date,
        index=True,
        nullable=False,
    )

    currency: Mapped["Currency"] = relationship(
        "Currency",
        back_populates="rates",
    )

    def __repr__(self) -> str:
        return (
            f"<ExchangeRate id={self.id} "
            f"currency_id={self.currency_id} "
            f"date={self.date} rate={self.rate}>"
        )
