from typing import Optional

from pydantic import BaseModel, Field


class ReqBodyBase(BaseModel):
    id: str = Field(max_length=64)
    callbackUrl: Optional[str] = Field(default=None, max_length=1024)
    callbackApiKey: Optional[str] = Field(default=None, max_length=3072)
    meta: Optional[str] = Field(default=None, max_length=128)
    """
    Флаг указывающий стоит ли игнорировать
    проверку КМ.
    Если флаг не указан, то для формирования
    чека все КМ должны успешно пройти
    проверку: в тэге 2106 биты номер 0, 1, 2, 3
    имеют состояние «1»
    Если же флаг не указан и КМ не прошел
    проверку чек не будет сформирован и
    запрос статуса будет возвращать статус 422
    Unprocessable Entity
    """
    ignoreItemCodeCheck: Optional[bool] = Field(default=None)
