from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app.models import HotTags, BestProfile, Profile

OBJS_ON_PAGE = 10

def get_cur_user(request):
    user_id = request.COOKIES.get('user_id')
    try:
        user = Profile.objects.get(id=user_id)
    except Profile.DoesNotExist:
        user = None
    return user

def base_context(request):
    user = get_cur_user(request)
    tags = HotTags.objects.get()
    users = BestProfile.objects.get()
    return {
               'user': user,
               'tags': tags,
               'users': users,
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
