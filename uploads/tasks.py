from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from time import sleep
from .models import UploadFile

import hashlib


@shared_task
def generate_checksums(pk):
    max_retries = 10
    retries = 0
    instance = None

    while(retries < max_retries):
        try:
            instance = UploadFile.objects.get(pk=pk)
            break
        except ObjectDoesNotExist:
            retries = retries + 1
            sleep(1)
            continue

    if not instance:
        return

    hash256 = hashlib.sha256()
    md5hash = hashlib.md5()

    # If file fits in memory it will be in one chunk
    with instance.file.open('rb') as f:
        for chunk in f.chunks():
            hash256.update(chunk)
            md5hash.update(chunk)

    instance.sha256sum = hash256.hexdigest()
    instance.md5sum = md5hash.hexdigest()
    instance.save()
