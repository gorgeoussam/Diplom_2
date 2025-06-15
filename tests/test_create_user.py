import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message
from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_create_user import HelpersOnCreateUser as u


@pytest.fixture
@allure.title('prepeare to delete user user')
def setup_user():

    TestCreateUser.to_teardown = False
    TestCreateUser.auth_token = None

    yield
    if TestCreateUser.to_teardown:
        u.try_to_delete_user(TestCreateUser.auth_token)


class TestCreateUser:

    to_teardown = False
    auth_token = None

    @allure.title('save user data for deletion')
    def __init_teardown(self, auth_token):
        TestCreateUser.to_teardown = True
        TestCreateUser.auth_token = auth_token


    @allure.title('test create unique user')
    def test_create_user_new_user(self, setup_user):

        user_data = u.generate_random_user_data()
        auth_token, refresh_token = u.create_and_check_user(user_data)
        self.__init_teardown(auth_token)


    @allure.title('create duplicate user')
    def test_create_user_double_user_error(self, setup_user):

        user_data = u.generate_random_user_data()
        auth_token, refresh_token = u.create_user(user_data)
        self.__init_teardown(auth_token)
        response = u.try_to_create_user(user_data)

        c.check_not_success_error_message(response, CODE.FORBIDDEN, message.USER_ALREADY_EXISTS)


    @allure.title('create user with missing field')
    @pytest.mark.parametrize('field', [
        KEYS.EMAIL_KEY,
        KEYS.PASSWORD_KEY,
        KEYS.NAME_KEY
    ])
    def test_create_user_empty_field_error(self, field):

        user_data = u.generate_random_user_data()
        user_data.pop(field)
        response = u.try_to_create_user(user_data)

        c.check_not_success_error_message(response, CODE.FORBIDDEN, message.MISSING_REQUIRED_FIELD)
