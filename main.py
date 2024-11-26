from controllers.basecontroller import BaseController
from models.database import get_session
from views.baseview import BaseView
from argon2 import PasswordHasher

from models.user import User
from models.client import Client

ph = PasswordHasher()

view = BaseView()
session = get_session()
controller = BaseController(view, session)

user = User.get_by_id(session, 1)

controller.user_creation(user)

# try:
#     ph.verify(user.password, "123456")
#     print("Password is correct!")
# except Exception as e:
#     print("Password verification failed:", e)

# client = Client.get_by_id(session, 1)
# client.sales_contact_id = user.id
# client.save(session)
# print(client)
