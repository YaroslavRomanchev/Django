from django.db import models
# Модель User предоставляет основу для создания пользователей в системе аутентификации
from django.contrib.auth.models import User
from PIL import Image #Библиотека для работы с изображениями

class Profile(models.Model):
    # OneToOneField означает, что каждому экземпляру Profile соответствует один единственный экземпляр User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # ImageField автоматически обрабатывает изображения и хранит их. 
    # Параметр default='default.jpg' указывает, что по умолчанию будет использовано изображение default.jpg
    # Параметр upload_to='user_images' указывает, что все загружаемые изображения будут сохранены в директории user_images
    img = models.ImageField(default='default.jpg', upload_to='user_images')

    # , будет выводиться строка "Профайл пользователя {self.user.username}", 
    # где {self.user.username} заменяется именем пользователя, ассоциированного с данным профилем. 
    # Это полезно для удобства идентификации объектов профиля.
    def __str__(self):
        return f'Профайл пользователя {self.user.username}'
    
    

# если вылезает ошибка, и пишет что на вход пришел какой то странный force_insert значит в функции save небыло дозаписано - *args, **kwargs
    def save(self, *args, **kwargs):# полиморфизм - перезаписывание существующей функции
        super().save() # все берем с родителя
        image = Image.open(self.img.path) # получаем наше изображение через наши каталоги

        if image.height > 256 or image.width > 256: # если параметы изображения больше 256 
            resize = (256, 256)
            image.thumbnail(resize) # обрезаем фото
            image.save(self.img.path) # сохраняем в тот каталог в котором она и находилась
