import base64
import json
from typing import Annotated
from urllib.parse import urljoin

import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from pydantic import BaseModel, StringConstraints, validate_call

from orangedatatools.schemas import (
    Correction12Schema,
    CorrectionSchema,
    DocumentSchema,
    ItemCodeSchema,
)
from orangedatatools.schemas.client_args import ClientArgs
from orangedatatools.utils.endpoints import OrangeEndpoints as ENDS

NonEmptyStr = Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]


class OrangeDataClient:
    @validate_call
    def __init__(
        self,
        org_params: ClientArgs,
        api_url: NonEmptyStr,
        key_private_path: NonEmptyStr,
        client_key_path: NonEmptyStr,
        client_cert_path: NonEmptyStr,
    ):
        """Initializes the client with the passed parameters.

        Args:
            org_params (Client Args): Organization parameters.
            api_url (str): The URL of the API for sending requests.
            key_private_path (str): The path to the private key for signing.
            client_key_path (str): The path to the client's private key.
            client_cert_path (str): The path to the client SSL certificate.
        """
        self.org_params = org_params
        self.__api_url = api_url.rstrip("/")
        self.__client_key_path = client_key_path
        self.__client_cert_path = client_cert_path

        self.__private_key = self.__readPrivateKey(key_private_path)

    def __combineData(self, data: BaseModel) -> dict:
        """Merging organization parameters and receipt data

        Args:
            data (BaseModel): Pydantic data schema
        """

        return {
            **self.org_params.model_dump(),
            **data.model_dump(exclude_none=True, mode="json"),
        }

    def __readPrivateKey(self, private_key_path: NonEmptyStr):
        with open(private_key_path, "rb") as pem_in:
            pemlines = pem_in.read()
        return load_pem_private_key(pemlines, password=None)

    def __computeSignature(self, data: bytes) -> str:
        """Creating a signature based on a private pem key"""
        signature = self.__private_key.sign(data, padding.PKCS1v15(), hashes.SHA256())

        return base64.b64encode(signature).decode("utf-8")

    @validate_call
    def __signPost(self, params: BaseModel, path: NonEmptyStr) -> tuple[str, int]:
        data = self.__combineData(params)
        bytes_data = json.dumps(data).encode("utf-8")
        sign = self.__computeSignature(bytes_data)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Signature": sign,
        }

        url_path = urljoin(self.__api_url, path)

        r = requests.post(
            url=url_path,
            headers=headers,
            json=data,
            cert=(self.__client_cert_path, self.__client_key_path),
            timeout=30,
        )

        return r.text, r.status_code

    @validate_call
    def __Get(self, path: NonEmptyStr) -> tuple[str, int]:
        url_path = urljoin(self.__api_url, path)
        r = requests.get(
            url=url_path,
            cert=(self.__client_cert_path, self.__client_key_path),
            timeout=30,
        )

        return r.text, r.status_code

    @validate_call
    def create_receipt(self, order_params: DocumentSchema) -> tuple[str, int]:
        return self.__signPost(order_params, ENDS.document())

    @validate_call
    def check_receipt(self, document_id: NonEmptyStr) -> tuple[str, int]:
        path = ENDS.document_status(self.org_params.inn, document_id)

        return self.__Get(path)

    @validate_call
    def create_correction(self, correction_params: CorrectionSchema) -> tuple[str, int]:
        return self.__signPost(correction_params, ENDS.corrections())

    @validate_call
    def check_correction(self, correction_id: NonEmptyStr) -> tuple[str, int]:
        path = ENDS.corrections_status(self.org_params.inn, correction_id)

        return self.__Get(path)

    @validate_call
    def create_correction12(
        self, correction_params: Correction12Schema
    ) -> tuple[str, int]:
        return self.__signPost(correction_params, ENDS.corrections12())

    @validate_call
    def check_correction12(self, correction_id: NonEmptyStr) -> tuple[str, int]:
        path = ENDS.correction12_status(self.org_params.inn, correction_id)

        return self.__Get(path)

    @validate_call
    def create_itemcode(self, itemcode_params: ItemCodeSchema) -> tuple[str, int]:
        return self.__signPost(itemcode_params, ENDS.itemcode())

    @validate_call
    def check_itemcode(self, itemcode_id: NonEmptyStr) -> tuple[str, int]:
        path = ENDS.itemcode_status(self.org_params.inn, itemcode_id)

        return self.__Get(path)
