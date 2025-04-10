from django.core.mail import EmailMultiAlternatives, send_mail

def send_test_email(target):
    subject = "Test Email"
    from_email = "test@mail.goosefarmersimulator.com"
    text_content = "This is an test message."
    html_content = "<p>This is an <strong>test</strong> message.</p>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [target])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_email_verification(target, code):
    print(target)
    subject = "Verify your Email"
    from_email = '"Goose Farmer Simulator" <verify@mail.goosefarmersimulator.com>'
    link = "https://goosefarmersimulator.com/guest-verify/" + code
    text_content = "Thank you for signing up. Use this link to verify your email: " + link + ". This link expires in 1 hour."
    html_content = "<p>Thank you for signing up.</p><p>Use this link to verify your email: <a href="+link+">"+link+"</a>\
        </p> <p>This link expires in 1 hour.</p>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [target])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
