from django.contrib import admin
from .models import Task, Board, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')  # Показываем имя и цвет тега
    search_fields = ('name',)  # Добавляем поиск по имени


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'created_at')  # Показываем название, цвет и дату создания
    search_fields = ('name',)  # Добавляем поиск по названию
    list_filter = ('color',)  # Фильтр по цвету


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'expired_at', 'assigned_to', 'created_at')  # Поля для отображения
    list_filter = ('board', 'tags', 'expired_at')  # Фильтры по доске, тегам и дате окончания
    search_fields = ('title', 'description')  # Поля для поиска
    autocomplete_fields = ('tags',)  # Автозаполнение тегов
    raw_id_fields = ('assigned_to', 'created_by')  # Упрощение выбора пользователей

