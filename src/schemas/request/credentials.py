from rest_framework import serializers


class CredentialsIn(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
