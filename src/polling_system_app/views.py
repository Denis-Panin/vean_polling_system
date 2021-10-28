from .generics import SurveySerializer, QuestionSerializer, ActivePollSerializer, AnswerSerializer
from rest_framework import viewsets
from .models import Survey, Question, ActivePoll, Answer


class SurveyAPIViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all().order_by('-id')
    serializer_class = SurveySerializer


class QuestionAPIViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-id')
    serializer_class = QuestionSerializer


class ActivePollAPIViewSet(viewsets.ModelViewSet):
    queryset = ActivePoll.objects.all().order_by('-id')
    serializer_class = ActivePollSerializer


class AnswerAPIViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all().order_by('-id')
    serializer_class = AnswerSerializer
