from decimal import Decimal
from enum import IntEnum
from typing import Optional

from pydantic import BaseModel, Field

from .base_args import ReqBodyBaseCorrection
from .common import DecimalField, TaxSystem


class CorrectionTypes(IntEnum):
    self_selected = 0  # выбрана самостоятельно
    prescribed = 1  # предписана (обязательна)


class CorrectionCalcIndicator(IntEnum):
    """Индикатор расчёта для чека коррекции (только доход/расход)."""

    income = 1
    expense = 3


class CorrectionSchemaContent(BaseModel):
    correctionType: CorrectionTypes
    type: CorrectionCalcIndicator
    causeDocumentDate: str
    causeDocumentNumber: Optional[str] = Field(default=None, max_length=32)
    totalSum: DecimalField = Field(decimal_places=2)
    cashSum: Optional[Decimal] = Field(default=None, decimal_places=2)
    eCashSum: Optional[Decimal] = Field(default=None, decimal_places=2)
    prepaymentSum: Optional[Decimal] = Field(default=None, decimal_places=2)
    postpaymentSum: Optional[Decimal] = Field(default=None, decimal_places=2)
    otherPaymentTypeSum: Optional[Decimal] = Field(default=None, decimal_places=2)
    tax1Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    tax2Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    tax3Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    tax4Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    tax5Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    tax6Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    tax7Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    tax8Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    tax9Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    tax10Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    taxationSystem: TaxSystem
    automatNumber: Optional[str] = Field(default=None, max_length=20)
    settlementAddress: Optional[str] = Field(default=None, max_length=243)
    settlementPlace: Optional[str] = Field(default=None, max_length=243)
    customerContact: str = Field(max_length=64)
    senderEmail: Optional[str] = Field(default=None, max_length=64)
    isInternetStore: Optional[bool] = Field(default=None)
    useTax20: Optional[bool] = Field(default=None)


class CorrectionSchema(ReqBodyBaseCorrection):
    content: CorrectionSchemaContent
