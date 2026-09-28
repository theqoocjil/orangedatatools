from decimal import Decimal
from enum import IntEnum
from typing import Annotated, Optional

from pydantic import BaseModel, Field, PlainSerializer
from pydantic_extra_types.phone_numbers import PhoneNumber

from .base_args import ReqBodyBase


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
    date: Optional[str]
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


class Contact(PhoneNumber):
    phone_format = "E164"


class SupplierInfoSchema(BaseModel):
    phoneNumbers: list[Contact]
    name: str = Field(max_length=239)


class AdditionalUserDetailsSchema(BaseModel):
    name: str = Field(max_length=64)
    value: str = Field(max_length=234)


class PaymentSchema(BaseModel):
    type: int = Field(ge=1, le=16)
    amount: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ] = Field(decimal_places=2)


class TaxSystem(IntEnum):
    osn = 0  # Общая (ОСН)
    usn_income = 1  # УСН «доходы»
    usn_profit = 2  # УСН «доходы минус расходы»
    envd = 3  # ЕНВД (отменён с 01.01.2021, оставлен для старых чеков)
    esn = 4  # ЕСХН
    patent = 5  # ПСН (патент)


class PaymentInfo(BaseModel):
    amount: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ] = Field(decimal_places=2)
    type: int = Field(le=255)
    id: str = Field(max_length=256)
    additionalInfo: str = Field(max_length=256)


class PaymentsInfo(BaseModel):
    payments: list[PaymentInfo]


class ReceiptClosingParametersSchema(BaseModel):
    payments: list[PaymentSchema]
    taxationSystem: TaxSystem
    electronicPaymentsInfo: PaymentsInfo


class VatRate(IntEnum):
    vat_20 = 1  # 20% (22% с 01.01.2026)
    vat_10 = 2  # 10%
    vat_20_120 = 3  # расч. 20/120 (22/122 с 01.01.2026)
    vat_10_110 = 4  # расч. 10/110
    vat_0 = 5  # 0%
    vat_none = 6  # не облагается
    vat_5 = 7  # 5%
    vat_7 = 8  # 7%
    vat_5_105 = 9  # расч. 5/105
    vat_7_107 = 10  # расч. 7/107


class PaymentMethod(IntEnum):
    prepayment_full = 1  # Предоплата 100%
    prepayment_partial = 2  # Частичная предоплата
    advance = 3  # Аванс
    full_payment = 4  # Полный расчёт
    partial_credit = 5  # Частичный расчёт и кредит
    credit = 6  # Передача в кредит
    credit_payment = 7  # Оплата кредита


class SettlementSubject(IntEnum):
    product = 1  # Товар
    excisable = 2  # Подакцизный товар
    work = 3  # Работа
    service = 4  # Услуга
    gambling_bet = 5  # Ставка азартной игры
    gambling_win = 6  # Выигрыш азартной игры
    lottery_ticket = 7  # Лотерейный билет
    lottery_win = 8  # Выигрыш лотереи
    ip_rights = 9  # Предоставление РИД
    advance = 10  # Платёж (аванс, задаток, предоплата, кредит)
    agent_fee = 11  # Агентское вознаграждение
    payout = 12  # Выплата (взнос, пеня, штраф, бонус)
    other_subject = 13  # Иной предмет расчёта
    property_right = 14  # Имущественное право
    non_op_income = 15  # Внереализационный доход
    other_payments = 16  # Иные платежи и взносы
    trading_fee = 17  # Торговый сбор
    tourist_tax = 18  # Туристический налог
    deposit = 19  # Залог
    expense = 20  # Расход
    pension_ip = 21  # Взносы на ОПС ИП (за себя)
    pension = 22  # Взносы на ОПС (за работников)
    medical_ip = 23  # Взносы на ОМС ИП (за себя)
    medical = 24  # Взносы на ОМС (за работников)
    social = 25  # Взносы на ОСС
    casino = 26  # Платёж казино
    cash_out = 27  # Выдача денежных средств
    unmarked_atnm = 30  # АТНМ (не имеющий кода маркировки)
    marked_atm = 31  # АТМ (имеющий код маркировки)
    tnm = 32  # ТНМ
    tm = 33  # ТМ


class PostionSchema(BaseModel):
    quantity: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ] = Field(decimal_places=6)
    price: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ] = Field(decimal_places=2)
    tax: VatRate
    taxSum: Optional[Decimal] = Field(default=None, decimal_places=2)
    text: str = Field(max_length=128)
    paymentMethodType: Optional[PaymentMethod] = Field(default=4)
    paymentSubjectType: Optional[SettlementSubject] = Field(default=1)
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


class CalcIndicator(IntEnum):
    income = 1
    income_return = 2
    expense = 3
    expense_return = 4


class DocumentSchemaContent(BaseModel):
    ffdVersion: Optional[int] = Field(default=2)
    type: CalcIndicator
    positions: list[PostionSchema]
    checkClose: ReceiptClosingParametersSchema
    customerContact: str = Field(max_length=64)
    agentType: Optional[int] = Field(default=None, le=127)
    paymentTransferOperatorPhoneNumbers: Optional[list[str]] = Field(default=None)
    paymentAgentOperation: Optional[str] = Field(default=None, max_length=24)
    paymentAgentPhoneNumbers: Optional[list[str]] = Field(default=None)
    paymentOperatorPhoneNumbers: Optional[list[str]] = Field(default=None)
    paymentOperatorName: Optional[str] = Field(default=None, max_length=64)
    paymentOperatorAddress: Optional[str] = Field(default=None, max_length=243)
    paymentOperatorINN: Optional[str] = Field(
        default=None, min_length=10, max_length=12
    )
    supplierPhoneNumbers: Optional[list[str]] = Field(default=None)
    additionalUserAttribute: Optional[AdditionalUserDetailsSchema] = Field(default=None)
    additionalAttribute: Optional[str] = Field(default=None, max_length=16)
    automatNumber: Optional[str] = Field(default=None, max_length=20)
    settlementAddress: Optional[str] = Field(default=None, max_length=243)
    settlementPlace: Optional[str] = Field(default=None, max_length=243)
    customer: Optional[str] = Field(default=None, max_length=243)
    customerINN: Optional[str] = Field(default=None, min_length=10, max_length=12)
    customerInfo: Optional[InformationBuyerSchema] = Field(default=None)
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
    # industryAttribute: ???? ссылается само на себя???


class DocumentSchema(ReqBodyBase):
    content: DocumentSchemaContent
