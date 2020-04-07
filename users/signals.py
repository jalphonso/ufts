from .models import Contract
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Contract)
def create_contract_group(sender, instance, **kwargs):
    # content_type = ContentType.objects.get_for_model(Contract)
    group, created = Group.objects.get_or_create(name=instance.name)
    view_permission = Permission.objects.get(codename="view_uploadfile",
                                             content_type__app_label="uploads")
    if created:
        group.permissions.add(view_permission)
