from django.db.models import Count, F
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Test, Question, Answer, UserAnswer
from .serializers import TestSerializer, QuestionSerializer, UserAnswerSerializer, AnswerSerializer


class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        question = request.data.get("question")
        user_answer = UserAnswer.objects.filter(username=username,
                                                question=question)
        if not user_answer.exists():
            return super().create(request, *args, **kwargs)
        else:
            user_answer.first().answer_id = request.data.get("answer")
            user_answer.first().save()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class TestResultView(APIView):

    @classmethod
    def get_total_pass(cls, test_id: int):
        total_questions = Question.objects.filter(test_id=test_id).count()
        users_pass = UserAnswer.objects.filter(question__test_id=test_id).values('username').annotate(
            total_answered=Count('question__test')).filter(total_answered=total_questions)
        return users_pass.count()

    @classmethod
    def get_success_questions(cls, test_id: int):
        total_questions = Question.objects.filter(test_id=test_id).count()
        users_and_correct_answers = UserAnswer.objects.filter(question__test_id=test_id,
                                                              answer__is_correct=True).values('username').annotate(
            correct_answers=Count('id'))
        successful_users_count = sum(
            1 for user in users_and_correct_answers if user['correct_answers'] > total_questions / 2)
        total_users_count = UserAnswer.objects.filter(question__test_id=test_id).values('username').distinct().count()
        success_rate = (successful_users_count / total_users_count) * 100
        return round(success_rate, 2)

    @classmethod
    def calculate_difficulty(cls, test_id):
        questions_with_percentage = Question.objects.filter(test_id=test_id).annotate(
            total_answers=Count('answers'),
            total_correct_answers=Count('answers', filter=F('answers__is_correct')),
            correct_percentage=(Count('answers', filter=F('answers__is_correct')) * 100) / Count('answers')
        )
        hardest_question = questions_with_percentage.order_by('correct_percentage').first()
        return hardest_question.text, hardest_question.correct_percentage

    def get(self, request, test_id):
        try:
            total_pass = self.get_total_pass(test_id)
            success_pass = self.get_success_questions(test_id)
            difficult_question = self.calculate_difficulty(test_id)
            result_data = {
                "total_attempts": total_pass,
                "success_pass": f'{success_pass}%',
                "difficult_question": difficult_question
            }

            return Response(result_data, status=status.HTTP_200_OK)
        except Test.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
