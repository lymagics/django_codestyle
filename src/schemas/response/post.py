from rest_framework import serializers

from database.models.post import Post
from schemas.response.user import UserOut


class PostOut(serializers.ModelSerializer):
    author = UserOut()

    class Meta:
        model = Post
        fields = ('id', 'text', 'created_at', 'author',)
