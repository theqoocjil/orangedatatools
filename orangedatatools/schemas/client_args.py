from pydantic import BaseModel, Field


class ClientArgs(BaseModel):
    inn: str = Field(min_length=10, max_length=12)
    group: str = Field(default=None, max_length=32)
    """
    Название ключа, который должен быть
    использован для проверки подписи. Для
    клиентов используется их ИНН, для новых
    клиентов с 01.02.25 ИНН_ID (ID -
    идентификационный номер
    пользователя в системе). Для партнеров
    и платежных агентов код с маской 301****,
    для вендинга 401****.
    """
    key: str = Field(max_length=32)
