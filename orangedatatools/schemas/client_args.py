from pydantic import BaseModel, Field


class ClientArgs(BaseModel):
    inn: str = Field(min_length=10, max_length=12)
    group: str = Field(default=None, max_length=32)
    key: str = Field(max_length=32)
