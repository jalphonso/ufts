from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from users.models import Contract
from jsa.models import Jsa


def home(request):
    contract_statuses = []
    now = datetime.now()

    try:
        contracts = request.user.groups.all()
        for contract in contracts:
            expiring = False
            try:
                contract_obj = Contract.objects.get(name__exact=contract)
                expiry_date = contract_obj.expiry_date
                warning_date = (now + timedelta(days=90)).date()
                if expiry_date and expiry_date <= warning_date:
                    expiring = True
                contract_statuses.append({'name': contract,
                                          'valid': True,
                                          'expiry_date': expiry_date,
                                          'expiring': expiring })
            except ObjectDoesNotExist:
                contract_statuses.append({'name': contract,
                                          'valid': False })

    except AttributeError as e:
        if "Anonymous" in str(e):
            pass

    recent_timeframe = (now - timedelta(days=30)).date()
    recent_jsas = Jsa.objects.filter(date__gte=recent_timeframe)

    context = {
        'contracts': contract_statuses,
        'jsas': recent_jsas
    }
    return render(request, 'home.html', context)
