from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

from app.utils import AjaxableResponseMixin
from app.models import Question, Profile

User = get_user_model()

class AdminUserAddForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'

class AdminUserChangeForm(UserChangeForm):
    class Meta:
        fields = '__all__'
        model = User

class QuestionForm(forms.ModelForm, AjaxableResponseMixin):
    def clean():
        pass
    def clean_tags():
        pass
    def save():
        pass
    class Meta:
        model = Question
        fields = (
            'title',
            'text',
            'tags',
        )
        lables = {
            'title': _('Title'),
        }
        help_texts = {
            'text': _('Text'),
        }
        error_messages = {
            'title': {
                'max_length': _('is too long'),
            },
            NON_FIELD_ERRORS: {
                'unique_together': _("%(model_name)s's %(field_lables)s are not unique."),
            },
        }
        localized_fields = '__all__'

class RegistrationForm(forms.ModelForm, AjaxableResponseMixin):
    def clean_user(self):
        pass
    
    class Meta:
        model = Profile
        fields = (
            'username',
            'password',
            'email',
            'avatar',
        )
        localized_fields = '__all__'
