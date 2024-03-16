import re

from backbone.service_layer.abstract_validator import AbstractValidator


class PhoneNumberValidator(AbstractValidator):
    def __init__(self, loc: str, phone_number: str):
        self.phone_number = phone_number
        super().__init__(loc)

    def type(self) -> str:
        return "invalid_phone_number"

    def passes(self) -> bool:
        return re.match(r"^(0)?9\d{9}$", self.phone_number) is not None


class EmailValidator(AbstractValidator):
    def __init__(self, loc: str, email: str):
        self.email = email
        super().__init__(loc)

    def type(self) -> str:
        return "invalid_email"

    def passes(self) -> bool:
        return re.match(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", self.email) is not None


class PostalCodeValidator(AbstractValidator):
    def __init__(self, loc: str, postal_code: str):
        self.postal_code = postal_code
        super().__init__(loc)

    def type(self) -> str:
        return "invalid_postal_code"

    def passes(self) -> bool:
        return re.match(r"\b(?!(\d)\1{3})[13-9]{4}[1346-9][013-9]{5}\b", self.postal_code) is not None
