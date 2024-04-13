from rest_framework import serializers

from database.models.post import Post


class PostIn(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('text',)
