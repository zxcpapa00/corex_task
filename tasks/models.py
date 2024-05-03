from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=100)


class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = models.BooleanField(default=False)
