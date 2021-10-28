# from rest_framework import serializers
#
# from .models import Survey, Question, ActivePoll, Answer
#
#
# class SurveySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Survey
#         fields = (
#             'survey_name',
#             'start_date',
#             'end_date',
#             'survey_description',
#         )
#
#
# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = (
#             'survey',
#             'text',
#             'type',
#         )
#
#
# class ActivePollSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ActivePoll
#         fields = (
#             'question',
#             'active_poll_text',
#         )
#
#
# class AnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Answer
#         fields = (
#             'user_id',
#             'survey',
#             'question',
#             'active_poll',
#             'active_poll_text',
#         )
from rest_framework import serializers
from .models import Survey, Question, ActivePoll, Answer


class CurrentUserDefault(object):
    def set_context(self, serializer_field):
        self.user_id = serializer_field.context['request'].user.id

    def __call__(self):
        return self.user_id


class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(default=CurrentUserDefault())
    survey = serializers.SlugRelatedField(queryset=Survey.objects.all(), slug_field='id')
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    active_poll = serializers.SlugRelatedField(queryset=ActivePoll.objects.all(), slug_field='id', allow_null=True)
    active_poll_text = serializers.CharField(max_length=250, allow_null=True, required=False)

    class Meta:
        model = Answer
        fields = '__all__'

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def validate(self, attrs):
        question_type = Question.objects.get(id=attrs['question'].id).question_type
        try:
            if question_type == "one" or question_type == "text":
                obj = Answer.objects.get(question=attrs['question'].id, survey=attrs['survey'],
                                         user_id=attrs['user_id'])
            elif question_type == "multiple":
                obj = Answer.objects.get(question=attrs['question'].id, survey=attrs['survey'],
                                         user_id=attrs['user_id'],
                                         active_poll=attrs['active_poll'])
        except Answer.DoesNotExist:
            return attrs
        else:
            raise serializers.ValidationError('Уже ответил')


class ActivePollSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    active_poll_text = serializers.CharField(max_length=250)

    def validate(self, attrs):
        try:
            obj = ActivePoll.objects.get(question=attrs['question'].id, active_poll_text=attrs['active_poll_text'])
        except ActivePoll.DoesNotExist:
            return attrs
        else:
            raise serializers.ValidationError('Выбор уже существует')

    class Meta:
        model = ActivePoll
        fields = '__all__'

    def create(self, validated_data):
        return ActivePoll.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    survey = serializers.SlugRelatedField(queryset=Survey.objects.all(), slug_field='id')
    question_text = serializers.CharField(max_length=250)
    question_type = serializers.CharField(max_length=250)
    active_poll = ActivePollSerializer(many=True, read_only=True)

    def validate(self, attrs):
        question_type = attrs['question_type']
        if question_type == 'one' or question_type == 'multiple' or question_type == 'text':
            return attrs
        raise serializers.ValidationError('Тип вопроса может быть только один, несколько или текстовый')

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class SurveySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    survey_name = serializers.CharField(max_length=200)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    survey_description = serializers.CharField(max_length=200)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = '__all__'

    def create(self, validated_data):
        return Survey.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'start_date' in validated_data:
            raise serializers.ValidationError({'start_date': 'Вы не можете изменять это поле.'})
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
