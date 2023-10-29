import sendgrid
from django.conf import settings

SENDGRID_API_KEY = settings.APP_CONF["OAUTH_CLIENT_SECRET"]
SUPPORT_EMAIL = 'scoder91@gmail.com'

def send_email(otp, recipient_email):
    # Create Mail
    message = sendgrid.helpers.mail.Mail(
        from_email=SUPPORT_EMAIL,
        to_emails=recipient_email,
        subject='Your OTP Code',
        html_content=f'''
                   <h1>Welcome to Social Media APP!</h1>
                   <p>Thank you for registering. Please use the OTP code below to verify your email address and complete the registration process.</p>
                   <h2>OTP Code: {otp}</h2>
                   <p>If you did not make this request, please ignore this email.</p>
               '''
    )

    # Send Mail using Sendgrid Client
    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    return sg.send(message)
