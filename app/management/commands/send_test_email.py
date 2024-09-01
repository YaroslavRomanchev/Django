from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = "Send a test email to verify SMTP settings."

    def handle(self, *args, **kwargs):
        subject = 'Test Email'
        message = 'This is a test email sent from Django.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['your-email@example.com']  # замените на ваш email

        try:
            send_mail(subject, message, from_email, recipient_list)
            self.stdout.write(self.style.SUCCESS('Successfully sent test email'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error sending email: {e}'))