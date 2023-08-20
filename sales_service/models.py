from enum import StrEnum


class ProductType(StrEnum):
    ...


class Crate:
    ...


class Customer:
    def get_warehouse_address_verified(self):
        ...


class Package:
    def __init__(self, crates: list[Crate], customer: Customer) -> None:
        ...
