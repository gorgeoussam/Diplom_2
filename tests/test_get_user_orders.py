import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message

from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_create_user import HelpersOnCreateUser as u
from helpers.helpers_on_get_ingredients import HelpersOnGetIngredients as g


@pytest.fixture(scope='class')
@allure.title('retrieve ingredients data and initialise')
def setup_ingredients():
    ingredients = g.get_ingredients()
    TestGetUserOrders.buns_list = g.get_buns_list(ingredients)
    TestGetUserOrders.fillings_list = g.get_fillings_list(ingredients)
    TestGetUserOrders.sauces_list = g.get_sauces_list(ingredients)
    c.check_ingredients(TestGetUserOrders.buns_list, TestGetUserOrders.fillings_list, TestGetUserOrders.sauces_list)


@pytest.mark.usefixtures('setup_ingredients', scope='class')
class TestGetUserOrders:

    buns_list = None
    fillings_list = None
    sauces_list = None


    @allure.step('assemble burger')
    def __create_burger(self):
        ingredients_list = [
            (self.buns_list[0])[KEYS.ID_KEY],
            (self.fillings_list[0])[KEYS.ID_KEY],
            (self.sauces_list[0])[KEYS.ID_KEY],
        ]
        return ingredients_list



    @allure.title('checl list of orders for authorised user')
    def test_get_user_orders_list_authorized_user(self, setup_user):

        user_data, auth_token = setup_user
        ingredients_list = self.__create_burger()
        u.create_order(ingredients_list, auth_token)
        response = u.try_to_get_user_orders(auth_token)

        received_body = c.check_success_ok(response)
        c.check_received_orders_list(received_body, 1)


    # 2
    @allure.title('check "total" orders for authorised users')
    def test_get_user_orders_total_authorized_user(self, setup_user):

        user_data, auth_token = setup_user
        ingredients_list = self.__create_burger()
        u.create_order(ingredients_list, auth_token)
        response = u.try_to_get_user_orders(auth_token)

        received_body = c.check_success_ok(response)
        c.check_received_orders_total(received_body, 1)


    # 3
    @allure.title('check total today for authorised user')
    def test_get_user_orders_total_today_authorized_user(self, setup_user):

        user_data, auth_token = setup_user
        ingredients_list = self.__create_burger()
        u.create_order(ingredients_list, auth_token)
        response = u.try_to_get_user_orders(auth_token)
        received_body = c.check_success_ok(response)
        c.check_received_orders_total_today(received_body, 1)


    @allure.title('authorised user no orders check')
    def test_get_user_orders_list_authorized_user_no_orders(self, setup_user):

        user_data, auth_token = setup_user
        response = u.try_to_get_user_orders(auth_token)

        received_body = c.check_success_ok(response)
        c.check_received_orders_list(received_body, 0)


    # 2
    @allure.title('total orders for authorised users without orders')
    def test_get_user_orders_total_authorized_user_no_orders(self, setup_user):

        user_data, auth_token = setup_user
        response = u.try_to_get_user_orders(auth_token)
        received_body = c.check_success_ok(response)
        c.check_received_orders_total(received_body, 0)


    # 3
    @allure.title('check "total today" for authorised user with no orders')
    def test_get_user_orders_total_today_authorized_user_no_orders(self, setup_user):

        user_data, auth_token = setup_user
        response = u.try_to_get_user_orders(auth_token)
        received_body = c.check_success_ok(response)
        c.check_received_orders_total_today(received_body, 0)


    @allure.title('anouthirised user orders check>error')
    def test_get_user_orders_unauthorized_user_error(self):

        response = u.try_to_get_user_orders()
        c.check_not_success_error_message(response, CODE.UNAUTHORIZED, message.UNAUTHORIZED)