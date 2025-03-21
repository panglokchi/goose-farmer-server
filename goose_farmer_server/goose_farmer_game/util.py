from django.core.mail import EmailMultiAlternatives, send_mail

def send_email_verification(target, code):
    send_mail(
            "Goose Farmer Simulator - Email Verification",
            "Email confirmation code:" + code,
            "mail@sandbox6653ff8c35494ffc861b67a59f13ac5a.mailgun.org",
            [target]
        )