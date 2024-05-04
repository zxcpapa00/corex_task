from django.urls import path
from .views import TestListCreateView, TestRetrieveUpdateDestroyView, QuestionCreateView, IndexView, TestDetailView

app_name = "tasks"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', TestDetailView.as_view(), name='test'),
    path('api/', TestListCreateView.as_view(), name='test-list'),
    path('api/<int:pk>/', TestRetrieveUpdateDestroyView.as_view(), name='test-detail'),
    path('api/question/', QuestionCreateView.as_view(), name='question-create')
]
