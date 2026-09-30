"""
Пример использования orangedatatools.

Все значения (ИНН, ключи, суммы) — тестовые заглушки.
Для реальной работы подставьте свои данные и пути к сертификатам.
"""

from orangedatatools.client import OrangeDataClient
from orangedatatools.schemas import (
    ClientArgs,
    CorrectionSchema,
    CorrectionSchemaContent,
    DocumentSchema,
    DocumentSchemaContent,
    ItemCodeSchema,
    ItemCodeSchemaContent,
    PaymentSchema,
    PostionSchema,
    ReceiptClosingParametersSchema,
)

ORG_PARAMS = ClientArgs(
    inn="123456789012",
    group="Main",
    key="123456789012",
)

CLIENT = OrangeDataClient(
    org_params=ORG_PARAMS,
    api_url="https://apip.orangedata.ru:2443",
    key_private_path="./values/private_key_test.crt",
    client_cert_path="./values/client.crt",
    client_key_path="./values/client.key",
)


def create_receipt(document_id: str) -> None:
    """Создать чек."""
    order_params = DocumentSchema(
        id=document_id,
        content=DocumentSchemaContent(
            type=1,
            positions=[
                PostionSchema(
                    quantity=1.000,
                    price=123.45,
                    tax=6,
                    text="Test",
                    paymentMethodType=4,
                    paymentSubjectType=1,
                )
            ],
            checkClose=ReceiptClosingParametersSchema(
                payments=[PaymentSchema(type=1, amount=123.45)],
                taxationSystem=1,
            ),
            customerContact="test@mail.ru",
        ),
    )

    print(CLIENT.create_receipt(order_params=order_params))


def check_receipt(document_id: str) -> None:
    """Проверить статус чека по его id."""
    print(CLIENT.check_receipt(document_id=document_id))


def create_correction(correction_id: str) -> None:
    """Создать документ коррекции."""
    correction = CorrectionSchema(
        id=correction_id,
        content=CorrectionSchemaContent(
            correctionType=1,
            type=1,
            causeDocumentDate="2017-08-10T00:00:00",
            causeDocumentNumber="AP-54",
            totalSum=17.25,
            cashSum=1.25,
            eCashSum=2.34,
            prepaymentSum=5.67,
            postpaymentSum=4.56,
            otherPaymentTypeSum=3.45,
            tax1Sum=1.34,
            tax2Sum=2.34,
            tax3Sum=3.34,
            tax4Sum=4.34,
            tax5Sum=5.34,
            tax6Sum=6.34,
            taxationSystem=1,
            automatNumber="123456789",
            settlementAddress="г. Москва, Красная площадь, д. 1",
            settlementPlace="palata",
            customerContact="test@mi.ru",
        ),
    )

    print(CLIENT.create_correction(correction_params=correction))


def check_correction(correction_id: str) -> None:
    """Проверить статус коррекции."""
    print(CLIENT.check_correction(correction_id=correction_id))


def create_item_code(item_code: str) -> None:
    """Создать документ по коду маркировки."""
    itemcode_params = ItemCodeSchema(
        id=item_code,
        content=ItemCodeSchemaContent(
            plannedStatus=1,
            itemCode=item_code,
        ),
    )

    print(CLIENT.create_itemcode(itemcode_params=itemcode_params))


def check_item_code(item_code: str) -> None:
    """Проверить статус кода маркировки."""
    print(CLIENT.check_itemcode(itemcode_id=item_code))
