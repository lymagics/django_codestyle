from database.models.user import User
from tasks.mail import mail_send_task


class MailService:
    """
    Mail service.
    """
    def send_greetings_email(self, user: User):
        mail_send_task.delay(
            subject='Thank you for registration!',
            email=user.email,
            template='mail/greetings.html',
            username=user.username,
        )
