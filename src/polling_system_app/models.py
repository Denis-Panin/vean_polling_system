from django.db import models


class Survey(models.Model):
    survey_name = models.CharField(max_length=250)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    survey_description = models.CharField(max_length=250)

    def __str__(self):
        return self.survey_name


class Question(models.Model):
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    type = models.CharField(max_length=250)

    def __str__(self):
        return self.text


class ActivePoll(models.Model):
    question = models.ForeignKey(Question, related_name='active_poll', on_delete=models.CASCADE)
    active_poll_text = models.CharField(max_length=250)

    def __str__(self):
        return self.active_poll_text


class Answer(models.Model):
    user_id = models.IntegerField()
    survey = models.ForeignKey(Survey, related_name='survey', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)
    active_poll = models.ForeignKey(ActivePoll, related_name='active_poll', on_delete=models.CASCADE, null=True)
    active_poll_text = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.active_poll_text
