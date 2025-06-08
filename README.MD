pytest -v ./tests - to run tests

tests/ - folder with testts:

tests/test_create_user.py - user creation
tests/test_login_user.py - user authorisation
tests/test_update_user.py - refreshing user data
tests/test_create_order.py - creating order
tests/test_get_user_orders.py - retreiving orders list
helpers/ - helpers

helpers/helpers_on_create_user.py - working with users and orders
helpers/helpers_on_get_ingredients.py - retrieving ingredients
helpers/helpers_on_requests.py - creating/retrieving order list
helpers/helpers_on_check_response.py - check responses