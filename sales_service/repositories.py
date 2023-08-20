from sales_service.models import Crate, ProductType


class CrateRepository:
    def find_by_type_limit(self, product_type: ProductType, sold_crates: int) -> Crate:
        ...

    def delete(self, crates: list[Crate]):
        ...
