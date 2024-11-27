from tests.conftest import test_db
from models.user import User

class TestModels:
    def test_user_model_manual_creation(self, test_db):
        test_user = User(
            name="test",
            surname="test",
            email="test@test.com",
            password="123456",
            role_id=1,
        )
        test_db.add(test_user)
        test_db.commit()
        test_db.refresh(test_user)

        # Assert
        assert test_user.id is not None
        assert test_user.name == "test"
        assert test_user.email == "test@test.com"
