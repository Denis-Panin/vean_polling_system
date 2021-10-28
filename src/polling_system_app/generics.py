from rest_framework import serializers

from .models import Survey, Question, ActivePoll, Answer


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = (
            'survey_name',
            'start_date',
            'end_date',
            'survey_description',
        )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'survey',
            'text',
            'type',
        )


class ActivePollSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivePoll
        fields = (
            'question',
            'active_poll_text',
        )


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'user_id',
            'survey',
            'question',
            'active_poll',
            'active_poll_text',
        )
