from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import UserViewSet  # Импортируем UserViewSet

# Создаем и настраиваем роутер для API
router = DefaultRouter()
router.register(r'users', UserViewSet)  # Регистрация UserViewSet

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('api/', include(router.urls)),  # API маршруты
    path('move_task/', views.move_task, name='move_task'),
]

