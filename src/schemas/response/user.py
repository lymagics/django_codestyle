from hashlib import md5

from rest_framework import serializers

from database.models.user import User


class UserOut(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar_url',)

    def get_avatar_url(self, obj) -> str:
        avatar_hash = md5(obj.email.encode()).hexdigest()
        return f'https://www.gravatar.com/avatar/{avatar_hash}?d=mp'
