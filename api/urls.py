from django.urls import path 

from .views import TodoCompleteList, TodoListCreate, TodoRetrieveUpdateDestroy, TodoComplete
from . import views

urlpatterns = [
    #API
    path('todos/', TodoListCreate.as_view()),
    path('todos/<int:pk>/', TodoRetrieveUpdateDestroy.as_view()),
    path('todos/<int:pk>/complete/', TodoComplete.as_view()),
    path('todos/completed/', TodoCompleteList.as_view()),

    #Auth
    path('signup/', views.signup),
    path('login/', views.login),
]
