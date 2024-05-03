from django.urls import path
from .views import TestListCreateView, TestRetrieveUpdateDestroyView

app_name = "tasks"

urlpatterns = [
    path('', TestListCreateView.as_view(), name='test-list'),
    path('<int:pk>/', TestRetrieveUpdateDestroyView.as_view(), name='test-detail'),
]
