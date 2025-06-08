import allure

from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_requests import Requests as r


#
# Вспомогательные методы для работы с ингредиентами
class HelpersOnGetIngredients:

    @staticmethod
    @allure.step('receive ingredients list')
    def try_to_get_ingredients():
        return r.request_on_get_ingredients()


    @staticmethod
    @allure.step('retrieve list of buns')
    def get_buns_list(ingredients):
        buns_list = []
        for item in ingredients:
            if item['type'] == 'bun':
                buns_list.append(item)
        return buns_list


    @staticmethod
    @allure.step('retrieve ingredients list')
    def get_fillings_list(ingredients):
        fillings_list = []
        for item in ingredients:
            if item['type'] == 'main':
                fillings_list.append(item)
        return fillings_list


    @staticmethod
    @allure.step('retrieve sauces list')
    def get_sauces_list(ingredients):
        sauces_list = []
        for item in ingredients:
            if item['type'] == 'sauce':
                sauces_list.append(item)
        return sauces_list



    @staticmethod
    @allure.step('retreive ingredients data')
    def get_ingredients():
        response = HelpersOnGetIngredients.try_to_get_ingredients()
        return c.check_ingredients_list(response)