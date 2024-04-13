from rest_framework import serializers

from database.models.user import User


class UserIn(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password',)
