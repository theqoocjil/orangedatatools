import base64
import json
from urllib.parse import urljoin

import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from pydantic import BaseModel, validate_call
from schemas import Correction12Schema, CorrectionSchema, DocumentSchema
from schemas.client_args import ClientArgs
from utils.endpoints import OrangeEndpoints as ENDS


class OrangeDataClient:
    @validate_call
    def __init__(
        self,
        org_params: ClientArgs,
        api_url: str,
        key_private_path: str,
        client_key_path: str,
        client_cert_path: str,
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
        self.api_url = api_url.rstrip("/")
        self.key_private_path = key_private_path
        self.client_key_path = client_key_path
        self.client_cert_path = client_cert_path

    def __combine_data(self, data: BaseModel) -> dict:
        """Merging organization parameters and receipt data

        Args:
            data (BaseModel): Pydantic data schema
        """

        return {
            **self.org_params.model_dump(),
            **data.model_dump(exclude_none=True, mode="json"),
        }

    def __computeSignature(self, data: bytes):
        """Creating a signature based on a private pem key"""

        with open(self.key_private_path, "rb") as pem_in:
            pemlines = pem_in.read()
        private_key = load_pem_private_key(pemlines, password=None)
        signature = private_key.sign(data, padding.PKCS1v15(), hashes.SHA256())

        return base64.b64encode(signature).decode("utf-8")

    @validate_call
    def create_receipt(self, order_params: DocumentSchema) -> tuple[str, int]:

        data = self.__combine_data(order_params)
        bytes_data = json.dumps(data, ensure_ascii=False).encode("utf-8")
        sign = self.__computeSignature(bytes_data)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Signature": sign,
        }

        url_path = urljoin(self.api_url, ENDS.document())

        r = requests.post(
            url=url_path,
            headers=headers,
            json=data,
            cert=(self.client_cert_path, self.client_key_path),
            verify=False,
        )

        return r.text, r.status_code

    def check_receipt(self, document_id: str):

        url_path = urljoin(
            self.api_url, ENDS.document_status(self.org_params.inn, document_id)
        )
        r = requests.get(url=url_path)

        return r.text, r.status_code

    @validate_call
    def create_correction(self, correction_params: CorrectionSchema) -> tuple[str, int]:
        data = self.__combine_data(correction_params)
        bytes_data = json.dumps(data, ensure_ascii=False).encode("utf-8")
        sign = self.__computeSignature(bytes_data)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Signature": sign,
        }

        url_path = urljoin(self.api_url, ENDS.corrections())

        r = requests.post(
            url=url_path,
            headers=headers,
            json=data,
            cert=(self.client_cert_path, self.client_key_path),
            verify=False,
        )

        return r.text, r.status_code

    def check_correction(self, correction_id: str):
        url_path = urljoin(
            self.api_url, ENDS.corrections_status(self.org_params.inn, correction_id)
        )
        r = requests.get(url=url_path)

        return r.text, r.status_code

    @validate_call
    def create_correction12(self, correction_params: Correction12Schema):
        data = self.__combine_data(correction_params)
        bytes_data = json.dumps(data, ensure_ascii=False).encode("utf-8")
        sign = self.__computeSignature(bytes_data)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Signature": sign,
        }

        url_path = urljoin(self.api_url, ENDS.corrections12())

        r = requests.post(
            url=url_path,
            headers=headers,
            json=data,
            cert=(self.client_cert_path, self.client_key_path),
            verify=False,
        )

        return r.text, r.status_code

    def check_correction12(self, correction_id: str) -> tuple[str, int]:
        url_path = urljoin(
            self.api_url, ENDS.correction12_status(self.org_params.inn, correction_id)
        )
        r = requests.get(url=url_path)

        return r.text, r.status_code

    @validate_call
    def create_itemcode(self, itemcode_params: BaseModel):
        pass

    def check_itemcode(self, itemcode_id: str) -> tuple[str, int]:
        url_path = urljoin(
            self.api_url, ENDS.itemcode_status(self.org_params.inn, itemcode_id)
        )
        r = requests.get(url=url_path)

        return r.text, r.status_code
