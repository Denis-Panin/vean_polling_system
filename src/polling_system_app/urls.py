# from django.urls import path
# from rest_framework.routers import DefaultRouter
#
# from .views import SurveyAPIViewSet, QuestionAPIViewSet, ActivePollAPIViewSet, AnswerAPIViewSet
#
# router = DefaultRouter()
# router.register(prefix='api/v1/survey', viewset=SurveyAPIViewSet, basename='survey')
# router.register(prefix='api/v1/question', viewset=QuestionAPIViewSet, basename='question')
# router.register(prefix='api/v1/active_poll', viewset=ActivePollAPIViewSet, basename='active_poll')
# router.register(prefix='api/v1/answer', viewset=AnswerAPIViewSet, basename='answer')
#
# urlpatterns = router.urls
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),

    path('api/v1/surveys/create/', views.survey_create, name='survey_create'),
    path('surveys/update/<int:survey_id>/', views.survey_update, name='survey_update'),
    path('surveys/view/', views.survey_view, name='survey_view'),
    path('surveys/view/active/', views.active_survey_view, name='active_survey_view'),

    path('question/create/', views.question_create, name='question_create'),
    path('question/update/<int:question_id>/', views.question_update, name='question_update'),

    path('active_poll/create/', views.active_poll_create, name='active_poll_create'),
    path('active_poll/update/<int:choice_id>/', views.active_poll_update, name='active_poll_update'),

    path('answer/create/', views.answer_create, name='answer_create'),
    path('answer/view/<int:user_id>/', views.answer_view, name='answer_view'),
    path('answer/update/<int:answer_id>/', views.answer_update, name='answer_update')

]
