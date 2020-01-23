from .models import History
from lib.utilities import do_user_logging


def index(request):
    company_history = History.objects.all().order_by('text')

    context = {'company_history': company_history}
    do_user_logging(request)
    return render(request, 'home.html', context)
