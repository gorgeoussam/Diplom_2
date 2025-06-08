import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message

from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_create_user import HelpersOnCreateUser as u
from helpers.helpers_on_get_ingredients import HelpersOnGetIngredients as g


@pytest.fixture(scope='class')
@allure.title('initialise ingredients list')
def setup_ingredients():
    ingredients = g.get_ingredients()
    TestCreateOrder.buns_list = g.get_buns_list(ingredients)
    TestCreateOrder.fillings_list = g.get_fillings_list(ingredients)
    TestCreateOrder.sauces_list = g.get_sauces_list(ingredients)
    c.check_ingredients(TestCreateOrder.buns_list, TestCreateOrder.fillings_list, TestCreateOrder.sauces_list)


@pytest.mark.usefixtures('setup_ingredients', scope='class')
class TestCreateOrder:

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


    @allure.title('authorised user creates an order')
    def test_create_order_authorized_user(self, setup_user):

        user_data, auth_token = setup_user
        ingredients_id_list = self.__create_burger()
        response = u.try_to_create_order(ingredients_id_list, auth_token)

        c.check_order_data(response)


    @allure.title('check order creation for authorised user')
    def test_create_order_two_orders_for_authorized_user(self, setup_user):

        user_data, auth_token = setup_user
        ingredients_id_list = self.__create_burger()
        response = u.try_to_create_order(ingredients_id_list, auth_token)
        c.check_order_data(response)
        response = u.try_to_create_order(ingredients_id_list, auth_token)

        c.check_order_data(response)


    @allure.title('check orrder creation without authorisation')
    def test_create_order_unauthorized(self):
        ingredients_id_list = self.__create_burger()
        response = u.try_to_create_order(ingredients_id_list)

        c.check_order_data(response)


    @allure.title('check order creation without ingredients')
    def test_create_order_no_ingredients(self):

        ingredients_id_list = []
        response = u.try_to_create_order(ingredients_id_list)

        c.check_not_success_error_message(response, CODE.BAD_REQUEST, message.NO_INGREDIENTS)


    @allure.title('wrong ingredient hash order creation')
    def test_create_order_invalid_ingredient_hash(self):

        ingredients_id_list = ['0000000000']
        response = u.try_to_create_order(ingredients_id_list)

        c.check_status_code(response, CODE.ERROR_500)