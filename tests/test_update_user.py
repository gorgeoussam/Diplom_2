import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message

from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_create_user import HelpersOnCreateUser as u


class TestUpdateUser:

    @allure.title('refresh user data for authorised user')
    @pytest.mark.parametrize('field', [
        KEYS.EMAIL_KEY,
        KEYS.NAME_KEY,
        KEYS.PASSWORD_KEY,
    ])
    def test_update_user_success(self, setup_user, field):
        user_data, auth_token = setup_user
        new_user_data = u.generate_random_user_data()
        update_data = user_data.copy()
        update_data[field] = new_user_data[field]
        payload = {
            field: update_data[field]
        }
        response = u.try_to_update_user(payload, auth_token)

        received_body = c.check_success_ok(response)
        c.check_user_data(received_body, update_data)


    @allure.title('refresh data of unauthorised user')
    @pytest.mark.parametrize('field', [
        KEYS.EMAIL_KEY,
        KEYS.NAME_KEY,
        KEYS.PASSWORD_KEY,
    ])
    def test_update_user_not_authorized_error(self, setup_user, field):
        user_data, auth_token = setup_user
        new_user_data = u.generate_random_user_data()
        update_data = user_data.copy()
        update_data[field] = new_user_data[field]
        payload = {
            field: update_data[field]
        }
        response = u.try_to_update_user(payload)
        c.check_not_success_error_message(response, CODE.UNAUTHORIZED, message.UNAUTHORIZED)
