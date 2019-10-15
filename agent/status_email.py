from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_status_email(name,receiver,ticket_number,ticket_status):
    # Creating message subject and sender
    subject = f'Your Ticket Status has changed'
    sender = 'brians931@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('email/status_email.txt',{"name": name,"ticket_number":ticket_number,"ticket_status":ticket_status})
    html_content = render_to_string('email/status_email.html',{"name": name,"ticket_number":ticket_number,"ticket_status":ticket_status})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()
