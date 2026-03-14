from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.product import Product


def extract_prices(products: list['Product']) -> list[float]:
    return [p.price for p in products]
