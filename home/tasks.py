from celery import shared_task
from datetime import date,timedelta
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from jsa.models import Jsa
from uploads.models import UploadFile
from users.models import CustomUser
from lib.utilities import convert_html_to_plain_text
from lib.utilities import generate_download_report_pdf, generate_upload_report_pdf
from lib.utilities import generate_download_report_xlsx, generate_upload_report_xlsx
from lib.utilities import generate_download_report_docx, generate_upload_report_docx
import os


@shared_task
def daily_email():
    today = date.today()
    recent_jsas = Jsa.objects.filter(date=today)
    recent_softwares = UploadFile.objects.filter(verified_date=today)

    if not (recent_jsas or recent_softwares):
        return

    email_list = []
    users = CustomUser.objects.all()
    for user in users:
        if user.subscribe_to_emails:
            email_list.append(user.email)

    context = {
        'jsas': recent_jsas,
        'softwares': recent_softwares,
        'classification': settings.CLASSIFICATION_TEXT,
        'classification_color': settings.CLASSIFICATION_BACKGROUND_COLOR
    }
    subject = f'{settings.CLASSIFICATION_TEXT_SHORT} Juniper UFTS Daily News {today}'
    email_body_html = get_template('daily_email.txt').render(context)
    email_body_plain = convert_html_to_plain_text(email_body_html)
    email_from = None
    email_to = None
    email_bcc = email_list
    if subject and email_body_plain and email_bcc:
        email = EmailMultiAlternatives(subject, email_body_plain, email_from, email_to, email_bcc)
        if email_body_html:
            email.attach_alternative(email_body_html, 'text/html')
        email.send()


@shared_task
def weekly_report_email():
    today = date.today()
    startdate= today - timedelta(days=7)
    email_list = []
    users = CustomUser.objects.all()
    for user in users:
        if user.is_staff:
            email_list.append(user.email)

    if settings.REPORT_FORMAT == 'pdf':
        dlreportfile=os.path.join(settings.BASE_DIR,'reports/download_report-') + str(today) + '.pdf'
        ulreportfile=os.path.join(settings.BASE_DIR,'reports/upload_report-') + str(today) + '.pdf'
        downloads = generate_download_report_pdf(os.path.join(settings.BASE_DIR,'logs/download.log'),dlreportfile,startdate,today)
        uploads = generate_upload_report_pdf(os.path.join(settings.BASE_DIR,'logs/upload.log'),ulreportfile,startdate,today)
    elif settings.REPORT_FORMAT == 'xlsx':
        dlreportfile=os.path.join(settings.BASE_DIR,'reports/download_report-') + str(today) + '.xlsx'
        ulreportfile=os.path.join(settings.BASE_DIR,'reports/upload_report-') + str(today) + '.xlsx'
        downloads = generate_download_report_xlsx(os.path.join(settings.BASE_DIR,'logs/download.log'),dlreportfile,startdate,today)
        uploads = generate_upload_report_xlsx(os.path.join(settings.BASE_DIR,'logs/upload.log'),ulreportfile,startdate,today)
    elif settings.REPORT_FORMAT == 'docx':
        dlreportfile=os.path.join(settings.BASE_DIR,'reports/download_report-') + str(today) + '.docx'
        ulreportfile=os.path.join(settings.BASE_DIR,'reports/upload_report-') + str(today) + '.docx'
        downloads = generate_download_report_docx(os.path.join(settings.BASE_DIR,'logs/download.log'),dlreportfile,startdate,today)
        uploads = generate_upload_report_docx(os.path.join(settings.BASE_DIR,'logs/upload.log'),ulreportfile,startdate,today)

    if not (downloads or uploads):
        return

    context = {
        'downloads': downloads,
        'uploads': uploads,
        'classification': settings.CLASSIFICATION_TEXT,
        'classification_color': settings.CLASSIFICATION_BACKGROUND_COLOR
    }
    subject = f'{settings.CLASSIFICATION_TEXT_SHORT} Juniper UFTS Weekly Upload/Download Report {today}'
    email_body_html = get_template('weekly_report.txt').render(context)
    email_body_plain = convert_html_to_plain_text(email_body_html)
    email_from = None
    email_to = None
    email_bcc = email_list
    if subject and email_body_plain and email_bcc:
        email = EmailMultiAlternatives(subject, email_body_plain, email_from, email_to, email_bcc)
        if email_body_html:
            email.attach_alternative(email_body_html, 'text/html')
        if downloads:
            email.attach_file(dlreportfile)
        if uploads:
            email.attach_file(ulreportfile)
        email.send()
