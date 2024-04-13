import factory
from factory.django import DjangoModelFactory

from database.models.post import Post
from database.models.user import User


class UserFactory(DjangoModelFactory):
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = 'testpass123'

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class PostFactory(DjangoModelFactory):
    text = factory.Faker('sentence')
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Post
