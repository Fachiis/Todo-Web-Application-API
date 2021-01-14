from rest_framework import generics, permissions
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .serializers import TodoSerializer, TodoCompleteSerializer
from todo.models import Todo



@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data["username"], password=data["password"])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({'error':'That username has already been taken. Please choose another username.'}, status=400)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(data['username'], password=data['password'])
        if user is None:
            token = Token.objects.create(user=user)

class TodoCompleteList(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        todo = Todo.objects.filter(user=user, datecompleted__isnull=False).order_by('-datecompleted')
        return todo


class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        todo = Todo.objects.filter(user=user, datecompleted__isnull=True)
        return todo
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        todo = Todo.objects.filter(user=user)
        return todo

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class TodoComplete(generics.UpdateAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        todo = Todo.objects.filter(user=user)
        return todo
    
    def perform_update(self, serializer):
        serializer.instance.datecompleted = timezone.now()
        serializer.save()
    
    
