from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from app.models import Question, Profile, Tag, Answer

User = get_user_model()

# TODO: validate HTTP tag : Referer

class AdminUserAddForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'

class AdminUserChangeForm(UserChangeForm):
    class Meta:
        fields = '__all__'
        model = User

class QuestionForm(forms.ModelForm):
    tags = forms.RegexField(max_length=255, regex='^([_A-Za-z0-9]+)(, [_A-Za-z0-9]+){0,2}$', required=False)
    def clean_tags(self):
        tags = self.cleaned_data['tags'].split(', ')
        tags = list(filter(lambda x: x != '', tags))
        if len(tags) > 3:
            raise forms.ValidationError(_('You must not specified more than three tags'), code='more_than_3_tags')
        return tags

    def save(self, *args, **kwargs):
        tags = []
        for t in self.cleaned_data['tags']:
            try:
                tag = Tag.objects.get(title=t)
            except ObjectDoesNotExist:
                tag = Tag()
                tag.title = t
                tag.save()
            tags.append(tag)
        kwargs['commit'] = False
        question = super(QuestionForm, self).save(*args, **kwargs)
        return question, tags

    class Meta:
        model = Question
        fields = (
            'title',
            'text',
        )

#TODO:
#        lables = {
#            'title': _('Title'),
#        }
#        help_texts = {
#            'text': _('Text'),
#        }
#        error_messages = {
#            'title': {
#                'max_length': _('is too long'),
#            },
#            NON_FIELD_ERRORS: {
#                'unique_together': _("%(model_name)s's %(field_lables)s are not unique."),
#            },
#       }
        localized_fields = '__all__'

class BaseUserForm(forms.ModelForm):
    def clean_user(self):
        pass

    class Meta:
        model = Profile
        fields = (
            'username',
            'first_name',
            'last_name',
            'password',
            'email',
            'avatar',
        )
        localized_fields = (
            'first_name',
            'last_name',
        )

class RegistrationForm(BaseUserForm):
    pass

class SettingsForm(BaseUserForm):
    password = forms.CharField(max_length=80, widget=forms.PasswordInput, required=False)
    avatar = forms.ImageField(max_length=1024, required=False)
    username = forms.CharField(max_length=1024, required=False)

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = (
            'text',
        )
