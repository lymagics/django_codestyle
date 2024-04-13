from django.conf import settings

import jwt

from services.jwt import JwtService


def test_encode_method():
    # given
    payload = {'user_id': 123}
    jwt_service = JwtService()

    # when
    actual_encoded_data = jwt_service.encode(payload=payload)

    # then
    expected_encoded_data = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
    assert actual_encoded_data == expected_encoded_data


def test_decode_method():
    # given
    payload = {'user_id': 123}
    encoded_data = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')

    # when
    jwt_service = JwtService()
    actual_payload = jwt_service.decode(jwt_token=encoded_data)

    # then
    assert actual_payload is not None
    assert 'user_id' in actual_payload
    assert actual_payload == payload
    assert actual_payload['user_id'] == payload['user_id']


def test_decode_method_returns_none_if_case_of_error():
    # given
    invalid_jwt = 'eyJhbGciOiJIUzI1.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIi.SflKxwRJSMeKKF2QT4fwpMeJf36P'

    # when
    jwt_service = JwtService()
    expected_none = jwt_service.decode(jwt_token=invalid_jwt)

    # then
    assert expected_none is None
