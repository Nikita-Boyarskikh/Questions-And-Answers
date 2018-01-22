from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from app.forms import AdminUserChangeForm, AdminUserAddForm
from app.models import Like, Answer, Question, Tag

User = get_user_model()  # pylint: disable=invalid-name


class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserAddForm
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password',
            )
        }),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'avatar',
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        (_('Important dates'), {
            'fields': (
                'last_login',
                'date_joined',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': (
                'wide',
            ),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
            )
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Like)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
