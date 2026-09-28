from typing import Optional

from pydantic import BaseModel, Field

from .base_args import ReqBodyBaseFiscal
from .common import DecimalField, FractionalQuantityMarkedProductSchema


class ItemCodeSchemaContent(BaseModel):
    plannedStatus: int = Field(le=256)
    itemCode: int = Field(ge=1, le=223)
    quantityMeasurementUnit: Optional[int] = Field(le=255, default=None)
    quantity: Optional[DecimalField]
    fractionalQuantity: Optional[FractionalQuantityMarkedProductSchema]


class ItemCodeSchema(ReqBodyBaseFiscal):
    content: ItemCodeSchemaContent
