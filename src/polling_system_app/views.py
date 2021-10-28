# from .generics import SurveySerializer, QuestionSerializer, ActivePollSerializer, AnswerSerializer
# from rest_framework import viewsets
# from .models import Survey, Question, ActivePoll, Answer
#
#
# class SurveyAPIViewSet(viewsets.ModelViewSet):
#     queryset = Survey.objects.all().order_by('-id')
#     serializer_class = SurveySerializer
#
#
# class QuestionAPIViewSet(viewsets.ModelViewSet):
#     queryset = Question.objects.all().order_by('-id')
#     serializer_class = QuestionSerializer
#
#
# class ActivePollAPIViewSet(viewsets.ModelViewSet):
#     queryset = ActivePoll.objects.all().order_by('-id')
#     serializer_class = ActivePollSerializer
#
#
# class AnswerAPIViewSet(viewsets.ModelViewSet):
#     queryset = Answer.objects.all().order_by('-id')
#     serializer_class = AnswerSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.utils import timezone

from .models import Question, Survey, ActivePoll, Answer
from .generics import SurveySerializer, QuestionSerializer, ActivePollSerializer, AnswerSerializer


@csrf_exempt
@api_view(["GET"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Пожалуйста, укажите имя пользователя и пароль'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Неверные учетные данные'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def survey_create(request):
    serializer = SurveySerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        survey = serializer.save()
        return Response(SurveySerializer(survey).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def survey_update(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    if request.method == 'PATCH':
        serializer = SurveySerializer(survey, data=request.data, partial=True)
        if serializer.is_valid():
            survey = serializer.save()
            return Response(SurveySerializer(survey).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        survey.delete()
        return Response("Опрос удален", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def survey_view(request):
    survey = Survey.objects.all()
    serializer = SurveySerializer(survey, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def question_create(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save()
        return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def question_update(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'PATCH':
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionSerializer(question).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return Response("Вопрос удален", status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def active_poll_create(request):
    serializer = ActivePollSerializer(data=request.data)
    if serializer.is_valid():
        active_poll = serializer.save()
        return Response(ActivePollSerializer(active_poll).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def active_poll_update(request, active_poll_id):
    active_poll = get_object_or_404(ActivePoll, pk=active_poll_id)
    if request.method == 'PATCH':
        serializer = ActivePollSerializer(active_poll, data=request.data, partial=True)
        if serializer.is_valid():
            active_poll = serializer.save()
            return Response(ActivePollSerializer(active_poll).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        active_poll.delete()
        return Response("Выбор удален", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def active_survey_view(request):
    survey = Survey.objects.filter(end_date__gte=timezone.now()).filter(pub_date__lte=timezone.now())
    serializer = SurveySerializer(survey, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def answer_create(request):
    serializer = AnswerSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        answer = serializer.save()
        return Response(AnswerSerializer(answer).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def answer_view(request, user_id):
    answers = Answer.objects.filter(user_id=user_id)
    serializer = AnswerSerializer(answers, many=True)
    return Response(serializer.data)


@api_view(['PATCH', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def answer_update(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'PATCH':
        serializer = AnswerSerializer(answer, data=request.data, partial=True)
        if serializer.is_valid():
            answer = serializer.save()
            return Response(AnswerSerializer(answer).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        answer.delete()
        return Response("Ответ удален", status=status.HTTP_204_NO_CONTENT)
