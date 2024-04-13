from typing import Optional

from django.conf import settings

import jwt


class JwtService:
    """
    Jwt Service.
    """
    def encode(self, payload: dict) -> str:
        return jwt.encode(
            payload=payload,
            key=settings.SECRET_KEY,
            algorithm='HS256',
        )

    def decode(self, jwt_token: str) -> Optional[dict]:
        try:
            return jwt.decode(
                jwt_token,
                key=settings.SECRET_KEY,
                algorithms=['HS256'],
            )
        except jwt.PyJWTError:
            return None
