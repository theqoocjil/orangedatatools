from pydantic import validate_call
from schemas.client_args import ClientArgs


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
