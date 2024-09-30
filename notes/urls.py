
from django.urls import path
from notes import views
from rest_framework.authtoken.views import ObtainAuthToken
urlpatterns=[
    path('register/', views.UserCreationView.as_view()),
    path('tasks/',views.TaskListCreateView.as_view()),
    path('tasks/<int:pk>/',views.TaskRetriveUpdateDestroyView.as_view()),
    path('tasks/summary/',views.TaskSummaryAPIView.as_view()),
    path('tasks/categories/',views.CategoryLIstView.as_view()),
    path('token/',ObtainAuthToken.as_view()),
]