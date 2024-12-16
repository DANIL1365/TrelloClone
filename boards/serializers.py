from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Board
from django.utils import timezone


# Валидация для пользователя (User)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

    def validate_username(self, value):
        """
        Проверка уникальности имени пользователя.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Это имя пользователя уже занято.")
        if len(value) < 3:
            raise serializers.ValidationError("Имя пользователя должно быть не короче 3 символов.")
        return value

    def validate_email(self, value):
        """
        Проверка уникальности email.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже зарегистрирован.")
        return value

    def validate(self, data):
        """
        Общая валидация для пользователя.
        """
        if len(data['username']) < 3:
            raise serializers.ValidationError("Имя пользователя должно быть не короче 3 символов.")

        if not data['email']:
            raise serializers.ValidationError("Поле 'email' не может быть пустым.")

        if '@' not in data['email']:
            raise serializers.ValidationError("Введите действительный email.")

        return data


# Валидация для задачи (Task)
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'expired_at', 'board', 'tags', 'assigned_to', 'created_by']

    def validate_title(self, value):
        """
        Проверка длины названия задачи и уникальности на доске.
        """
        if len(value) > 20:
            raise serializers.ValidationError("Название задачи не может превышать 20 символов.")

        board = self.initial_data.get('board')
        if Task.objects.filter(title=value, board=board).exists():
            raise serializers.ValidationError("Задача с таким названием уже существует на этой доске.")

        return value

    def validate_description(self, value):
        """
        Проверка длины описания задачи (максимум 2000 символов).
        """
        if len(value) > 2000:
            raise serializers.ValidationError("Описание задачи не может превышать 2000 символов.")
        return value

    def validate_expired_at(self, value):
        """
        Проверка, чтобы дата окончания задачи не была в прошлом.
        """
        if value < timezone.now():
            raise serializers.ValidationError("Дата окончания задачи не может быть раньше текущего времени.")
        return value

    def validate(self, data):
        """
        Общая валидация задачи.
        """
        if not data.get('expired_at'):
            raise serializers.ValidationError("Поле 'expired_at' должно быть указано.")

        return data
