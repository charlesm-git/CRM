from commands.authenticationcommands import AuthenticationController
from commands.usercommands import BaseController
from database import get_session
from views.authenticationview import AuthenticationView
from views.userview import UserView
from argon2 import PasswordHasher

from models.user import User
from models.client import Client

ph = PasswordHasher()

session = get_session()

view = UserView()
auth_view = AuthenticationView()

auth_controller = AuthenticationController(auth_view, session)
controller = BaseController(view, session, auth_controller)

user = auth_controller.login()
print(user)
if user:
    controller.user_creation(user)

# client = Client.get_by_id(session, 1)
# client.sales_contact_id = user.id
# client.save(session)
# print(client)


# user = auth_controller.login()
# if auth_controller.valid_token():
#     auth_controller.logout()
