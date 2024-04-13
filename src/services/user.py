from typing import Optional

from database.models.user import User


class UsersService:
    """
    Users service.
    """
    def create(self, email: str, username: str, password: str) -> User:
        user = User(email=email, username=username)
        user.set_password(password)
        user.full_clean()
        user.save()
        return user

    def get_by_id(self, id: int) -> Optional[User]:
        return User.objects.filter(id=id).first()
