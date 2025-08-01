import allure
import pytest

from helpers.helpers_on_create_user import HelpersOnCreateUser as u


@pytest.fixture
@allure.title('creating and deleting user')
def setup_user():
    # генерируем данные нового пользователя: email, password, user_name
    user_data = u.generate_random_user_data()
    # отправляем запрос на создание пользователя
    auth_token, refresh_token = u.create_user(user_data)
    # сохраняем полученные данные пользователя
    yield user_data, auth_token

    # Удаляем созданного пользователя
    u.try_to_delete_user(auth_token)
