class OrangeEndpoints:
    BASE = "/api/v2"

    @classmethod
    def check(cls) -> str:
        """
        GET-method
        """
        return f"{cls.BASE}/"

    @classmethod
    def document(cls) -> str:
        """
        POST-method
        """
        return f"{cls.BASE}/documents"

    @classmethod
    def correction(cls) -> str:
        """
        POST-method
        """
        return f"{cls.BASE}/correction12"

    @classmethod
    def itemcode(cls) -> str:
        """
        POST-method
        """
        return f"{cls.BASE}/itemcode"

    @classmethod
    def corrections(cls) -> str:
        """
        POST-method
        """
        return f"{cls.BASE}/corrections"

    @classmethod
    def document_status(cls, inn: str, document_id: str) -> str:
        """
        GET-method
        """
        return f"{cls.documents()}/{inn}/status/{document_id}"

    @classmethod
    def itemcode_status(cls, inn: str, itemcode: str) -> str:
        """
        GET-method
        """
        return f"{cls.itemcode()}/{inn}/status/{itemcode}"

    @classmethod
    def corrections_status(cls, inn: str, correction_id: str) -> str:
        """
        GET-method
        """
        return f"{cls.corrections()}/{inn}/status/{correction_id}"

    @classmethod
    def correction12_status(cls, inn: str, correction_id: str) -> str:
        """
        GET-method
        """
        return f"{cls.correction12()}/{inn}/status/{correction_id}"
