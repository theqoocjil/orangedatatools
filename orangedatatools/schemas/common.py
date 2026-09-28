from decimal import Decimal
from enum import IntEnum
from typing import Annotated, Optional

from pydantic import BaseModel, Field, PlainSerializer
from pydantic_extra_types.phone_numbers import PhoneNumber

DecimalField = Annotated[
    Decimal,
    PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
]


class TaxSystem(IntEnum):
    osn = 0
    usn_income = 1
    usn_profit = 2
    envd = 3
    esn = 4
    patent = 5


class CalcIndicator(IntEnum):
    income = 1
    income_return = 2
    expense = 3
    expense_return = 4


class VatRate(IntEnum):
    vat_20 = 1
    vat_10 = 2
    vat_20_120 = 3
    vat_10_110 = 4
    vat_0 = 5
    vat_none = 6
    vat_5 = 7
    vat_7 = 8
    vat_5_105 = 9
    vat_7_107 = 10


class PaymentMethod(IntEnum):
    prepayment_full = 1
    prepayment_partial = 2
    advance = 3
    full_payment = 4
    partial_credit = 5
    credit = 6
    credit_payment = 7


class SettlementSubject(IntEnum):
    product = 1
    excisable = 2
    work = 3
    service = 4
    gambling_bet = 5
    gambling_win = 6
    lottery_ticket = 7
    lottery_win = 8
    ip_rights = 9
    advance = 10
    agent_fee = 11
    payout = 12
    other_subject = 13
    property_right = 14
    non_op_income = 15
    other_payments = 16
    trading_fee = 17
    tourist_tax = 18
    deposit = 19
    expense = 20
    pension_ip = 21
    pension = 22
    medical_ip = 23
    medical = 24
    social = 25
    casino = 26
    cash_out = 27
    unmarked_atnm = 30
    marked_atm = 31
    tnm = 32
    tm = 33


class Contact(PhoneNumber):
    phone_format = "E164"


class FractionalQuantityMarkedProductSchema(BaseModel):
    Numerator: Optional[int] = Field(default=None)
    Denominator: Optional[int] = Field(default=None)


class BarcodesCalculationItem(BaseModel):
    ean8: Optional[str] = Field(default=None, max_length=8)
    ean13: Optional[str] = Field(default=None, max_length=13)
    itf14: Optional[str] = Field(default=None, max_length=14)
    gs1: Optional[str] = Field(default=None, max_length=38)
    mi: Optional[str] = Field(default=None, max_length=20)
    egais20: Optional[str] = Field(default=None, max_length=23)
    egais30: Optional[str] = Field(default=None, max_length=14)
    f1: Optional[str] = Field(default=None, max_length=32)
    f2: Optional[str] = Field(default=None, max_length=32)
    f3: Optional[str] = Field(default=None, max_length=32)
    f4: Optional[str] = Field(default=None, max_length=32)
    f5: Optional[str] = Field(default=None, max_length=32)
    f6: Optional[str] = Field(default=None, max_length=32)


class OperationalDetailsSchema(BaseModel):
    date: Optional[str] = Field(default=None)
    id: Optional[int] = Field(default=None, le=255)
    value: Optional[str] = Field(default=None, max_length=64)


class InformationBuyerSchema(BaseModel):
    name: Optional[str] = Field(default=None, max_length=239)
    inn: Optional[str] = Field(default=None, min_length=10, max_length=12)
    birthDate: Optional[str] = Field(default=None, max_length=10)
    citizenship: Optional[str] = Field(default=None, max_length=3)
    identityDocumentCode: Optional[str] = Field(default=None, max_length=2)
    identityDocumentData: Optional[str] = Field(default=None, max_length=64)
    address: Optional[str] = Field(default=None, max_length=239)


class AgentDataSchema(BaseModel):
    paymentTransferOperatorPhoneNumbers: list[str]
    paymentAgentOperation: str = Field(max_length=24)
    paymentAgentPhoneNumbers: list[str]
    paymentOperatorName: str = Field(max_length=64)
    paymentOperatorAddress: str = Field(max_length=243)
    paymentOperatorINN: str = Field(min_length=10, max_length=12)


class SupplierInfoSchema(BaseModel):
    phoneNumbers: list[Contact]
    name: str = Field(max_length=239)


class AdditionalUserDetailsSchema(BaseModel):
    name: str = Field(max_length=64)
    value: str = Field(max_length=234)


class PaymentSchema(BaseModel):
    type: int = Field(ge=1, le=16)
    amount: DecimalField = Field(decimal_places=2)


class PaymentInfo(BaseModel):
    amount: DecimalField = Field(decimal_places=2)
    type: int = Field(le=255)
    id: str = Field(max_length=256)
    additionalInfo: str = Field(max_length=256)


class PaymentsInfo(BaseModel):
    payments: list[PaymentInfo]


class ReceiptClosingParametersSchema(BaseModel):
    payments: list[PaymentSchema]
    taxationSystem: TaxSystem
    electronicPaymentsInfo: PaymentsInfo


class PostionSchema(BaseModel):
    quantity: DecimalField = Field(decimal_places=6)
    price: DecimalField = Field(decimal_places=2)
    tax: VatRate
    taxSum: Optional[Decimal] = Field(default=None, decimal_places=2)
    text: str = Field(max_length=128)
    paymentMethodType: Optional[PaymentMethod] = Field(
        default=PaymentMethod.full_payment
    )
    paymentSubjectType: Optional[SettlementSubject] = Field(
        default=SettlementSubject.product
    )
    nomenclatureCode: Optional[bytes] = Field(default=None, min_length=8, max_length=32)
    itemCode: Optional[str] = Field(default=None, max_length=233)
    plannedStatus: Optional[int] = Field(default=None, le=256)
    supplierInfo: Optional[SupplierInfoSchema] = Field(default=None)
    supplierINN: Optional[str] = Field(default=None, min_length=10, max_length=12)
    agentType: Optional[int] = Field(default=None, ge=1, le=127)
    agentInfo: Optional[AgentDataSchema] = Field(default=None)
    unitOfMeasurement: Optional[str] = Field(default=None, max_length=16)
    quantityMeasurementUnit: Optional[int] = Field(default=None, le=255)
    additionalAttribute: Optional[str] = Field(default=None, max_length=64)
    manufacturerCountryCode: Optional[str] = Field(default=None, max_length=3)
    customsDeclarationNumber: Optional[str] = Field(default=None, max_length=32)
    excise: Optional[Decimal] = Field(default=None, decimal_places=2)
    unitTaxSum: Optional[Decimal] = Field(default=None, decimal_places=2)
    fractionalQuantity: Optional[FractionalQuantityMarkedProductSchema] = Field(
        default=None
    )
    barcodes: Optional[BarcodesCalculationItem] = Field(default=None)
    assignedStatus: Optional[int] = Field(default=None)


class BaseContent(BaseModel):
    ffdVersion: Optional[int] = Field(default=2)
    type: CalcIndicator
    positions: list[PostionSchema]
    checkClose: ReceiptClosingParametersSchema
    customerContact: str = Field(max_length=64)
    additionalUserAttribute: Optional[AdditionalUserDetailsSchema] = Field(default=None)
    additionalAttribute: Optional[str] = Field(default=None, max_length=16)
    automatNumber: Optional[str] = Field(default=None, max_length=20)
    settlementAddress: Optional[str] = Field(default=None, max_length=243)
    settlementPlace: Optional[str] = Field(default=None, max_length=243)
    cashier: Optional[str] = Field(default=None, max_length=64)
    cashierINN: Optional[str] = Field(default=None, min_length=12)
    senderEmail: Optional[str] = Field(default=None, max_length=64)
    totalSum: Optional[Decimal] = Field(default=None, decimal_places=2)
    vat1Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    vat2Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    vat3Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    vat4Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    vat5Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    vat6Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    vat7Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    vat8Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    vat9Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    vat10Sum: Optional[Decimal] = Field(default=None, decimal_places=2)
    operationalAttribute: Optional[OperationalDetailsSchema] = Field(default=None)
    timeZone: Optional[int] = Field(default=None, ge=1, le=11)
    isInternetStore: Optional[bool] = Field(default=None)
    useTax20: Optional[bool] = Field(default=None)
