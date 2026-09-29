from typing import Optional

from pydantic import BaseModel, Field

from .base_args import ReqBodyBaseFiscal
from .common import DecimalField, FractionalQuantityMarkedProductSchema


class ItemCodeSchemaContent(BaseModel):
    plannedStatus: int = Field(le=256)
    itemCode: str = Field(min_length=1, max_length=223)
    quantityMeasurementUnit: Optional[int] = Field(le=255, default=None)
    quantity: Optional[DecimalField] = Field(default=None)
    fractionalQuantity: Optional[FractionalQuantityMarkedProductSchema] = Field(
        default=None
    )


class ItemCodeSchema(ReqBodyBaseFiscal):
    content: ItemCodeSchemaContent
