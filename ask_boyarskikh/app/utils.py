from django.http import JsonResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache

from app.models import Profile

OBJS_ON_PAGE = 20

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

def get_cur_user(request):
    user_id = request.COOKIES.get('user_id')
    try:
        user = Profile.objects.get(id=user_id)
    except Profile.DoesNotExist:
        user = None
    return user

def base_context(request):
    user = get_cur_user(request)
    tags = cache.get('hot_tags')
    best_users = cache.get('best_users')
    return {
               'user': user,
               'bestusers': best_users,
               'tags': tags,
               'error': None,
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

    context = base_context(request)
    context.update({
                       'objects': objects,
                       'page_range': page_range,
                       'cur_page': cur_page,
                       'pref_page_index': pref_page_index,
                       'next_page_index': next_page_index,
                   })
    return context
