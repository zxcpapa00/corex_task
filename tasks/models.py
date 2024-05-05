from django.db import models
from rest_framework.exceptions import ValidationError


class Test(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    username = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.question_id != self.answer.question_id:
            raise ValidationError("Ответ не относиться к этому вопросу")
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return self.question.text
