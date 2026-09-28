from typing import Optional

from pydantic import Field

from .base_args import ReqBodyBaseFiscal
from .common import BaseContent, Contact, InformationBuyerSchema


class DocumentSchemaContent(BaseContent):
    agentType: Optional[int] = Field(default=None, le=127)
    paymentTransferOperatorPhoneNumbers: Optional[list[Contact]] = Field(default=None)
    paymentAgentOperation: Optional[str] = Field(default=None, max_length=24)
    paymentAgentPhoneNumbers: Optional[list[Contact]] = Field(default=None)
    paymentOperatorPhoneNumbers: Optional[list[Contact]] = Field(default=None)
    paymentOperatorName: Optional[str] = Field(default=None, max_length=64)
    paymentOperatorAddress: Optional[str] = Field(default=None, max_length=243)
    paymentOperatorINN: Optional[str] = Field(
        default=None, min_length=10, max_length=12
    )
    supplierPhoneNumbers: Optional[list[Contact]] = Field(default=None)
    customer: Optional[str] = Field(default=None, max_length=243)
    customerINN: Optional[str] = Field(default=None, min_length=10, max_length=12)
    customerInfo: Optional[InformationBuyerSchema] = Field(default=None)


class DocumentSchema(ReqBodyBaseFiscal):
    content: DocumentSchemaContent
