from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task, Board
import json

# ViewSet для обработки запросов пользователей
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Ограничение доступа только для аутентифицированных пользователей

# Функция для домашней страницы
def home(request):
    boards = Board.objects.all()  # Получаем все доски
    return render(request, 'boards/home.html', {'boards': boards})

# Представление для перемещения задачи
@csrf_exempt
def move_task(request):
    if request.method == 'POST':
        try:
            # Загружаем данные из тела запроса
            data = json.loads(request.body)
            task_id = data.get('task_id')
            board_id = data.get('board_id')

            # Находим задачу и доску
            task = Task.objects.get(id=task_id)
            board = Board.objects.get(id=board_id)

            # Перемещаем задачу на новую доску
            task.board = board
            task.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid method.'})
