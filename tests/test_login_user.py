import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message
from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_create_user import HelpersOnCreateUser as u


class TestLoginUser:

    @allure.title('check authorisation of existing user')
    def test_login_user_success(self, setup_user):

        user_data, auth_token = setup_user
        response = u.try_to_login_user(user_data[KEYS.EMAIL_KEY], user_data[KEYS.PASSWORD_KEY])

        c.check_status_code(response, CODE.OK)
        received_body = c.check_success(response, True)
        c.check_new_user_data(received_body, user_data)


    @allure.title('authorisation with bad credentials')
    @pytest.mark.parametrize('field', [
        KEYS.PASSWORD_KEY,
        KEYS.EMAIL_KEY,
    ])
    def test_login_user_invalid_login_or_password_error(self, setup_user, field):

        user_data, auth_token = setup_user
        new_user_data = user_data.copy()
        new_user_data[field] = ""
        response = u.try_to_login_user(new_user_data[KEYS.EMAIL_KEY], new_user_data[KEYS.PASSWORD_KEY])
        c.check_not_success_error_message(response, CODE.UNAUTHORIZED, message.INVALID_LOGIN)