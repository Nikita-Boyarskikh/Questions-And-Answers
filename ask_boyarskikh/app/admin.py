from django.contrib import admin
from app.models import Answer, Profile, Question, Tag, HotTags

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(HotTags)
