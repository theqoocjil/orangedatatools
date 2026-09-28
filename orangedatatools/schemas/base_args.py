from typing import Optional

from pydantic import BaseModel, Field


class ReqBodyBase(BaseModel):
    id: str = Field(max_length=64)
    callbackUrl: Optional[str] = Field(default=None, max_length=1024)
    callbackApiKey: Optional[str] = Field(default=None, max_length=3072)
    meta: Optional[str] = Field(default=None, max_length=128)


class _IgnoreItemCodeCheckMixin(BaseModel):
    """Mixin with the common flag ignoreItemCodeCheck."""

    ignoreItemCodeCheck: Optional[bool] = Field(default=None)


class ReqBodyBaseFiscal(ReqBodyBase, _IgnoreItemCodeCheckMixin):
    """Base schema for fiscal documents."""

    pass


class ReqBodyBaseCorrection(ReqBodyBase):
    """Base schema for correction receipts."""

    pass


class ReqBodyBaseCorrection12(ReqBodyBase, _IgnoreItemCodeCheckMixin):
    """Base schema for correction receipts (format 1.2)."""

    pass
