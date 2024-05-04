from rest_framework import generics
from django.views.generic import ListView, DetailView
from .models import Test, Question
from .serializers import TestSerializer, QuestionSerializer


class TestListCreateView(generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class QuestionCreateView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class TestRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class IndexView(ListView):
    template_name = 'index.html'
    queryset = Test.objects.all()


class TestDetailView(DetailView):
    template_name = 'test.html'
    queryset = Test.objects.all()
