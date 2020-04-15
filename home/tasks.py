from celery import shared_task
from datetime import date
from django.core.mail import EmailMessage
from django.template.loader import get_template
from jsa.models import Jsa
from uploads.models import UploadFile
from users.models import CustomUser


@shared_task
def daily_email():
    today = date.today()
    recent_jsas = Jsa.objects.filter(date=today)
    recent_softwares = UploadFile.objects.filter(verified_date=today)
    email_list = []
    users = CustomUser.objects.all()
    for user in users:
        email_list.append(user.email)

    context = {
        'jsas': recent_jsas,
        'softwares': recent_softwares,
    }
    subject = f'Juniper UFTS Daily News {today}'
    email_body = get_template('daily_email.txt').render(context)
    email_from = None
    email_to = None
    email_bcc = email_list
    if subject and email_body and email_bcc:
        email = EmailMessage(
            subject,
            email_body,
            email_from,
            email_to,
            email_bcc,
        )
        email.send()