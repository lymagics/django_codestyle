from typing import Optional

from database.models.post import Post
from database.models.user import User


class PostsService:
    """
    Posts service.
    """
    def create(self, text: str, author: User) -> Post:
        post = Post(text=text, author=author)
        post.full_clean()
        post.save()
        return post

    def get_by_id(self, id: int) -> Optional[Post]:
        return Post.objects.filter(id=id).first()

    def get_list(self, limit: int, offset: int) -> list[Post]:
        return Post.objects.all()[offset:limit+offset]

    def get_count(self) -> int:
        return Post.objects.count()
