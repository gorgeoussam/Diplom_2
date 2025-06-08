import allure
import random
import string

from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_requests import Requests as r

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS


class HelpersOnCreateUser:


    @staticmethod
    def generate_random_string(length):
        """
        Метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки.
        :param length: (int) длина строки
        :return: (str) строка
        """
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string


    @staticmethod
    @allure.step('create new user')
    def try_to_create_user(user_data):
        return r.request_on_create_user(user_data)


    @staticmethod
    @allure.step('user authorisation')
    def try_to_login_user(email, password):
        payload = {KEYS.EMAIL_KEY: email, KEYS.PASSWORD_KEY: password}
        return r.request_on_login_user(payload)


    @staticmethod
    @allure.step('delete user')
    def try_to_delete_user(auth_token):
        headers = {KEYS.AUTH_TOKEN_KEY: auth_token}
        return r.request_on_delete_user(headers)


    @staticmethod
    @allure.step('refresh user data')
    def try_to_update_user(user_data, auth_token=None):
        if auth_token is not None:
            headers = {KEYS.AUTH_TOKEN_KEY: auth_token}
        else:
            headers = None
        return r.request_on_update_user(user_data, headers)


    @staticmethod
    @allure.step('logout user')
    def try_to_logout_user(token):
        payload = {KEYS.TOKEN_KEY: token}
        return r.request_on_logout_user(payload)



    @staticmethod
    @allure.step('create order')
    def try_to_create_order(ingredient_list, auth_token=None):  # ingredient_list
        if auth_token is not None:
            headers = {
                KEYS.AUTH_TOKEN_KEY: auth_token,  # "Autorization": auth_token
            }
        else:
            headers = None

        payload = {
            KEYS.INGREDIENTS: ingredient_list,
        }
        return r.request_on_create_order(payload, headers)


    @staticmethod
    @allure.step('retrieve order list')
    def try_to_get_user_orders(auth_token=None):
        if auth_token is not None:
            headers = {
                KEYS.AUTH_TOKEN_KEY: auth_token,  # "Autorization": auth_token
            }
        else:
            headers = None
        return r.request_on_get_user_orders(headers)



    @staticmethod
    @allure.step('generating user data: email, password, name')
    def generate_random_user_data():
        email = HelpersOnCreateUser.generate_random_string(10) + '@mail.ru'
        password = HelpersOnCreateUser.generate_random_string(10)
        name = HelpersOnCreateUser.generate_random_string(10)

        user_data = {
            KEYS.EMAIL_KEY: email,  # "email"
            KEYS.PASSWORD_KEY: password,  # "password"
            KEYS.NAME_KEY: name  # "name"
        }

        return user_data


    @staticmethod
    @allure.step('generating user name')
    def generate_random_user_name():
        return HelpersOnCreateUser.generate_random_string(10)


    @staticmethod
    @allure.step('generating email')
    def generate_random_user_login():
        return HelpersOnCreateUser.generate_random_string(10) + '@mail.ru'


    @staticmethod
    @allure.step('generating password')
    def generate_random_user_password():
        return HelpersOnCreateUser.generate_random_string(10)



    @staticmethod
    @allure.step('create new user')
    def create_and_check_user(user_data=None):

        if user_data is None:
            user_data = HelpersOnCreateUser.generate_random_user_data()

        response = HelpersOnCreateUser.try_to_create_user(user_data)
        received_body = c.check_success(response, True)
        auth_token, refresh_token = c.check_new_user_data(received_body, user_data)
        return auth_token, refresh_token



    @staticmethod
    @allure.step('create new user')
    def create_user(user_data=None):

        if user_data is None:
            user_data = HelpersOnCreateUser.generate_random_user_data()

        response = HelpersOnCreateUser.try_to_create_user(user_data)
        c.check_status_code(response, CODE.OK)
        received_body = response.json()
        auth_token = received_body[KEYS.ACCESS_TOKEN]
        refresh_token = received_body[KEYS.REFRESH_TOKEN]
        return auth_token, refresh_token


    @staticmethod
    @allure.step('create order and check response data')
    def create_order(ingredient_list, auth_token=None):

        response = HelpersOnCreateUser.try_to_create_order(ingredient_list, auth_token)
        c.check_status_code(response, CODE.OK)
        received_body = c.check_success(response, True)
        order_name = c.check_key_in_body(received_body, KEYS.NAME_KEY)
        received_order_data = c.check_key_in_body(received_body, KEYS.ORDER_KEY)
        order_number = c.check_key_in_body(received_order_data, KEYS.NUMBER_KEY)

        return order_number, order_name