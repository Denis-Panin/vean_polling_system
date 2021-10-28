from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SurveyAPIViewSet, QuestionAPIViewSet, ActivePollAPIViewSet, AnswerAPIViewSet

router = DefaultRouter()
router.register(prefix='survey', viewset=SurveyAPIViewSet, basename='survey')
router.register(prefix='question', viewset=QuestionAPIViewSet, basename='question')
router.register(prefix='active_poll', viewset=ActivePollAPIViewSet, basename='active_poll')
router.register(prefix='answer', viewset=AnswerAPIViewSet, basename='answer')

urlpatterns = router.urls
