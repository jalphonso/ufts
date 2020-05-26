from .models import Contract, CustomUser
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import get_template


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
            'type': kwargs['action']
        }
        subject = 'Contract membership changed'
        email_body = get_template('contract_changed_email.txt').render(context)
        email_from = None
        email_to = [instance.email]
        email = EmailMessage(
            subject,
            email_body,
            email_from,
            email_to,
        )
        email.send()