from django.db import models # обезательный класс для работы с моделями
from django.utils import timezone # класс для постановки реального времени(при публикации)
from django.contrib.auth.models import User # модель по работе с пользователями
from django.urls import reverse # фукнция для быстрого перенаправления на другую страницу(по имени из urls.py)

# Create your models here.
# Все эти атрибуты это как бы название стоблцов в базе данных нужных для заполнения определенной информации
class News(models.Model):
    title = models.CharField(max_length=100) # Макс. кол во символов
    text = models.TextField() # Текст
    date = models.DateTimeField(default=timezone.now) # Дата
    avtor = models.ForeignKey(User, on_delete=models.CASCADE) # Автор

    
    
    # эта функцию нужна чтобы отображать загаловок статьи в название старницы 
    def __str__(self): 
        return self.title
    
    # Перенаправление когда уже написали статью и отправляем ее 
    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk':self.pk})