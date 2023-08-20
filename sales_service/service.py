from sales_service.models import Customer, Package, ProductType
from sales_service.repositories import CrateRepository


class DeliveryService:
    def send(self, package: Package):
        ...


class Sales:
    def __init__(self, crate_repository: CrateRepository, delivery_service: DeliveryService):
        self._crate_repository = crate_repository
        self._delivery_service = delivery_service

    def sell(self, sold_crates: int, product_type: ProductType, customer: Customer):
        crates = self._crate_repository.find_by_type_limit(product_type, sold_crates)

        if sold_crates > len(crates):
            return False

        if customer.get_warehouse_address_verified():
            package_to_deliver = Package(crates, customer)
            self._delivery_service.send(package_to_deliver)
            self._crate_repository.delete(crates)
            return True

        return False
