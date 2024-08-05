
from django.conf import settings
from django.core.mail import EmailMessage




def send_account_activation_email(email,email_token):
    subject = 'your account needs to be verified'
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi,click on the link to activate your account http://127.0.0.1:8000/accounts/activate/{email_token}'

    email=EmailMessage(
        subject=subject,
        body=message,
        from_email=email_from,
        to=[email]

    )
    email.send()
    print('email sent succesfully')


def send_invoice(email,invoice_pdf):
    subject = 'Thank you for your order!'
    email_from = settings.EMAIL_HOST_USER
    msg = f"Please find attached invoice of your recent purchase."

    email = EmailMessage(
        subject=subject,
        body=msg,
        from_email=email_from,
        to=[email]
    )
    email.attach_file(invoice_pdf)
    email.send()

    print('invoice sent successfully')

