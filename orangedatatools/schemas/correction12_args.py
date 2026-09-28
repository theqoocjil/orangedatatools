from pydantic import Field

from .base_args import ReqBodyBaseCorrection12
from .common import BaseContent


class Correction12SchemaContent(BaseContent):
    correctionType: str
    causeDocumentDate: str
    causeDocumentNumber: str


class Correction12Schema(ReqBodyBaseCorrection12):
    content: Correction12SchemaContent
