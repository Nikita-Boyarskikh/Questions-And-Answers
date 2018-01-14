from json import dumps

from django.http import HttpResponse
from django.http import JsonResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.utils.translation import ugettext as _

from app.models import Profile

OBJS_ON_PAGE = 20

class HttpResponseAjax(HttpResponse):
    def __init__(self, status='ok', **kwargs):
        kwargs['status'] = status
        super(HttpResponseAjax, self).__init__(
            content = dumps(kwargs),
            content_type = 'application/json'
        )

class HttpResponseAjaxError(HttpResponseAjax):
    def __init__(self, code, message):
        super(HttpResponseAjaxError, self).__init__(
            status = 'error',
            code = code,
            message = message
        )

def login_required_ajax(view):
    def view2(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view(request, *args, **kwargs)
        elif request.is_ajax():
            return HttpResponseAjaxError(
                code = 'no_auth',
                message = _('Login is required'),
            )
        else:
            redirect('/login/?next=' + request.get_full_path())
    return view2

def base_context():
    tags = cache.get('hot_tags')
    best_user_ids = cache.get('bestusers')
    if not best_user_ids:
        best_users = []
    else:
        best_users = [ Profile.objects.get(id=u) for u in best_user_ids ]
    return {
               'bestusers': best_users,
               'tags': tags,
               'hide_text': True,
           }

def paginated_context(request, objects):
    paginator = Paginator(objects, OBJS_ON_PAGE)
    try:
        cur_page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    try:
        objects = paginator.page(cur_page)
    except EmptyPage:
        cur_page = paginator.num_pages
        objects = paginator.page(cur_page)

    first_page_in_range = cur_page - 2 if cur_page - 2 > 0 else 1
    last_page_in_range = cur_page + 2 if cur_page + 2 < paginator.num_pages else paginator.num_pages
    page_range = range(first_page_in_range, last_page_in_range + 1)
    pref_page_index = first_page_in_range - len(page_range)
    next_page_index = len(page_range) + len(page_range)//2

    context = base_context()
    context.update({
                       'objects': objects,
                       'page_range': page_range,
                       'cur_page': cur_page,
                       'pref_page_index': pref_page_index,
                       'next_page_index': next_page_index,
                   })
    return context
