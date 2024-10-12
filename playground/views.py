from django.core.mail import BadHeaderError, mail_admins, send_mail
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage


def say_hello(request):
    try:
        message = BaseEmailMessage(
            template_name='emails/email.html',
            context={
                'name': 'Issa'
            },
        )
        message.send(['issa@gmail.com'])
        mail_admins('subject', 'message', html_message='message')
    except BadHeaderError:
        pass
    
    return render(request, 'hello.html', {'name': 'Issa'})