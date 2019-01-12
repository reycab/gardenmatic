"""."""
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def send_email_notification(subject, ctx, to):
    """."""
    message = render_to_string(
        'account/email/email_notification.html', ctx)
    recipient_list = [to]
    msg = EmailMessage(
        subject,
        message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list)
    msg.content_subtype = 'html'
    msg.send(fail_silently=True)
