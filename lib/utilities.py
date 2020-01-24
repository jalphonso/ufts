import logging


def do_user_logging(request, action='query'):
    """
    Write page user activity info to log.
    :param request: The request posted to the page.
    :param action:
    the action being logged

    :return:
    """
    logger = logging.getLogger('project_user')
    request_data = ''
    for k, v in request.POST.lists():
        if k not in ('csrfmiddlewaretoken', 'submit', 'submit_records', 'searchBtn', 'sid'):
            request_data = request_data + k + ':'
            for x in v:
                request_data = request_data + x + '|'
    referer = request.META.get('HTTP_REFERER') or ''
    path = request.path or ''
    method = request.method or ''
    logger.info("|action: " + action + "|" + "method: " + method + "|" + "path: " + path + "|" + "http_referer: " + referer + "|" + "userid: " + str(request.user) + "|" + request_data)
    # Track the pages that the user visits
    if 's_pages_visited' in request.session:
        all_pages = request.session['s_pages_visited']
        if path not in request.session['s_pages_visited']:
            all_pages = all_pages + path + '|'
            request.session['s_pages_visited'] = all_pages
    else:
        request.session['s_pages_visited'] = str(str(request.user)) + ':' + path + '|'
    logger.info('|Pages visited by: ' + str(request.session['s_pages_visited']))
