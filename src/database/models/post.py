from django.db import models

from database.models.base import BaseModel
from database.models.user import User


class Post(BaseModel):
    """
    Post entity.
    """
    text = models.CharField(max_length=180)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='posts')
