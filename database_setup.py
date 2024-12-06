from rich import print

from models.user import User
from models.base import Base
from models.role import Role
from utils.validation import hash_password
from database import Session, engine


def initialize_database():
    Base.metadata.create_all(engine)

    with Session() as session:
        roles = [
            Role(name="sales"),
            Role(name="management"),
            Role(name="support"),
        ]
        
        session.add_all(roles)
        session.commit()

        user = User(
            name="admin",
            surname="admin",
            email="admin@admin.com",
            password=hash_password("admin"),
            role_id=2,
        )
        session.add(user)
        session.commit()

    print("[green]Database initialized successfully[/green]")


if __name__ == "__main__":
    initialize_database()
