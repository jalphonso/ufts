from celery import shared_task
from datetime import date
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template
from jsa.models import Jsa
from uploads.models import UploadFile
from users.models import CustomUser
from lib.utilities import generate_download_report_pdf, generate_upload_report_pdf
import os

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

@shared_task
def weekly_report_email():
    today = date.today()
    email_list = []
    users = CustomUser.objects.all()
    for user in users:
        email_list.append(user.email)
    dlreportfile=os.path.join(settings.BASE_DIR,'reports/download_report-') + str(today) + '.pdf'
    ulreportfile=os.path.join(settings.BASE_DIR,'reports/upload_report-') + str(today) + '.pdf'
    downloads = generate_download_report_pdf(os.path.join(settings.BASE_DIR,'logs/download.log'),dlreportfile)
    uploads = generate_upload_report_pdf(os.path.join(settings.BASE_DIR,'logs/upload.log'),ulreportfile)
    context = {
        'downloads': downloads,
        'uploads': uploads,
    }
    subject = f'Juniper UFTS Weekly Upload/Download Report {today}'
    email_body = get_template('weekly_report.txt').render(context)
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
        if downloads > 0:
            email.attach_file(dlreportfile)
        if uploads > 0:
            email.attach_file(ulreportfile)
        email.send()