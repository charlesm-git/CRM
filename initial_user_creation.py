from models.user import User
from utils.validation import hash_password
from database import Session

with Session() as session:
    user = User(
        name="admin",
        surname="admin",
        email="admin@admin.com",
        password=hash_password("admin"),
        role_id=2,
    )
    session.add(user)
    session.commit()
