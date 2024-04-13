import pytest
from pytest_mock import MockerFixture

from services.mail import MailService
from tests.factories import UserFactory


@pytest.mark.django_db
def test_send_greetings_email(mocker: MockerFixture):
    # given
    user = UserFactory()
    mock_mail_send_task = mocker.patch('services.mail.mail_send_task.delay')

    # when
    mail_service = MailService()
    mail_service.send_greetings_email(user=user)

    # then
    mock_mail_send_task.assert_called_once_with(
        subject='Thank you for registration!',
        email=user.email,
        template='mail/greetings.html',
        username=user.username,
    )
