"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product
from homework.models import Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(1000)
        assert product.check_quantity(999)
        assert product.check_quantity(0)
        assert product.check_quantity(1001) == False
        assert product.check_quantity(-1) == ValueError

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(0)
        assert product.check_quantity(1000)
        product.buy(500)
        assert product.check_quantity(500)
        product.buy(500)
        assert product.check_quantity(0)

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(1001)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product):
        cart.add_product(product, 5)
        assert cart.products[product] == 5

    def test_default_value_in_cart(self, cart, product):
        cart.add_product(product)
        assert cart.products[product] == 1

    def test_remove_product(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 4)
        assert cart.products[product] == 1

    def test_remove_more_than_in_cart_products(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 6)
        assert product not in cart.products

    def test_amount_for_remove_is_none(self, cart, product):
        cart.add_product(product, 10)
        cart.remove_product(product, None)
        assert product not in cart.products

    def test_clear_cart(self, cart, product):
        cart.add_product(product, 10)
        cart.clear()
        assert product not in cart.products

    def test_get_total_price(self, cart, product):
        cart.add_product(product, 15)
        assert cart.get_total_price() == 1500

    def test_get_total_price_when_ziro(self, cart, product):
        cart.add_product(product, 0)
        assert cart.get_total_price() == 0

    def test_get_total_price_default(self, cart, product):
        cart.add_product(product)
        assert cart.get_total_price() == 100

    def test_buy(self, cart, product):
        cart.add_product(product, 100)
        cart.buy()
        assert product.quantity == 900

    def test_buy_extra_amount(self, cart, product):
        cart.add_product(product, 1001)
        with pytest.raises(ValueError):
            cart.buy()
