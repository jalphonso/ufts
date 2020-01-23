from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'product_name': settings.PRODUCT_NAME,
        'company': settings.COMPANY_NAME,
        'address': settings.COMPANY_ADDRESS,
        'phone': settings.COMPANY_PHONE,
        'code_owner': settings.OWNER,
        'license_key': settings.LICENSE_KEY,
        'access_code': settings.ACCESS_CODE,
}