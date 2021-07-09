from .models import Contract, CustomUser
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import get_template
from lib.utilities import convert_html_to_plain_text


@receiver(post_save, sender=Contract)
def create_contract_group(sender, instance, **kwargs):
    # content_type = ContentType.objects.get_for_model(Contract)
    group, created = Group.objects.get_or_create(name=instance.name)
    view_permission = Permission.objects.get(codename="view_uploadfile",
                                             content_type__app_label="uploads")
    if created:
        group.permissions.add(view_permission)


@receiver(m2m_changed, sender=CustomUser.groups.through)
def notify_user_of_contract_change(sender, instance, **kwargs):
    accepted_signals = ['post_add', 'post_remove']

    if kwargs['action'] not in accepted_signals or kwargs['model'] != Group:
        return

    for pk in kwargs['pk_set']:
        group = Group.objects.get(id=pk)

        context = {
            'user': instance.first_name,
            'group': group,
            'permissions': group.permissions.all(),
            'type': kwargs['action'],
            'classification': settings.CLASSIFICATION_TEXT,
            'classification_color': settings.CLASSIFICATION_BACKGROUND_COLOR
        }
        subject = f'{settings.CLASSIFICATION_TEXT_SHORT} Contract membership changed'
        email_body_html = get_template('contract_changed_email.txt').render(context)
        email_body_plain = convert_html_to_plain_text(email_body_html)
        email_from = None
        email_to = [instance.email]
        email = EmailMultiAlternatives(subject, email_body_plain, email_from, email_to)
        if email_body_html:
            email.attach_alternative(email_body_html, 'text/html')
        email.send()
