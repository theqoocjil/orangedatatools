from typing import Optional

from pydantic import BaseModel, Field


class ReqBodyBase(BaseModel):
    id: str = Field(max_length=64)
    callbackUrl: Optional[str] = Field(default=None, max_length=1024)
    callbackApiKey: Optional[str] = Field(default=None, max_length=3072)
    meta: Optional[str] = Field(default=None, max_length=128)


class _IgnoreItemCodeCheckMixin(BaseModel):
    """Миксин с общим флагом ignoreItemCodeCheck."""

    ignoreItemCodeCheck: Optional[bool] = Field(default=None)


class ReqBodyBaseFiscal(ReqBodyBase, _IgnoreItemCodeCheckMixin):
    """Базовая схема для фискальных документов."""

    pass


class ReqBodyBaseCorrection(ReqBodyBase):
    """Базовая схема для чеков коррекции."""

    pass


class ReqBodyBaseCorrection12(ReqBodyBase, _IgnoreItemCodeCheckMixin):
    """Базовая схема для чеков коррекции (формат 1.2)."""

    pass
