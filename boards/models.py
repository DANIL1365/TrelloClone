from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


# Модель для тега (Tag)
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7)  # Цвет тега (например, #FF5733)

    def __str__(self):
        return self.name


# Модель для доски (Board)
class Board(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Уникальность названия доски
    color = models.CharField(max_length=7, default='#D3D3D3')  # Цвет доски (по умолчанию светло-серый)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Модель для задачи (Task)
class Task(models.Model):
    title = models.CharField(max_length=20)  # Название задачи (макс 20 символов)
    description = models.TextField(max_length=2000)  # Описание задачи (макс 2000 символов)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()  # Дата окончания задачи
    board = models.ForeignKey(Board, related_name='tasks', on_delete=models.CASCADE)  # Связь с доской
    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True)  # Связь с тегами (многие ко многим)
    assigned_to = models.ForeignKey(User, related_name='tasks_assigned', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='tasks_created', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def clean(self):
        """
        Кастомная валидация:
        - Проверка на уникальность названия задачи
        - Проверка, что дата окончания задачи не раньше текущей
        """
        # Проверка на уникальность названия задачи
        if Task.objects.filter(title=self.title).exclude(id=self.id).exists():
            raise ValidationError("Задача с таким названием уже существует.")

        # Проверка, что дата окончания задачи не может быть раньше текущей
        if self.expired_at < timezone.now():
            raise ValidationError("Дата окончания задачи не может быть в прошлом.")

        super().clean()  # Важно вызвать метод родительского класса
