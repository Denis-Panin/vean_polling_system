from django.contrib import admin

from .models import Survey, Question, ActivePoll, Answer

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(ActivePoll)
admin.site.register(Answer)
