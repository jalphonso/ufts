from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from users.models import Contract
from jsa.models import Jsa
from uploads.models import UploadFile


def home(request):
    contract_statuses = []
    now = date.today() 

    try:
        contracts = request.user.groups.all()
        for contract in contracts:
            expiring = False
            expired = False
            try:
                contract_obj = Contract.objects.get(name__exact=contract)
                expiry_date = contract_obj.expiry_date
                warning_date = now + timedelta(days=90)
                if expiry_date and expiry_date < now:
                    expired = True
                elif expiry_date and expiry_date <= warning_date:
                    expiring = True
                contract_statuses.append({'name': contract,
                                          'valid': True,
                                          'expiry_date': expiry_date,
                                          'expired': expired,
                                          'expiring': expiring })
            except ObjectDoesNotExist:
                contract_statuses.append({'name': contract,
                                          'valid': False })

    except AttributeError as e:
        if "Anonymous" in str(e):
            pass

    recent_timeframe = now - timedelta(days=30)
    recent_jsas = Jsa.objects.filter(date__gte=recent_timeframe)
    recent_softwares = UploadFile.objects.filter(verified_date__gte=recent_timeframe)

    context = {
        'contracts': contract_statuses,
        'jsas': recent_jsas,
        'softwares': recent_softwares,
    }
    return render(request, 'home.html', context)
