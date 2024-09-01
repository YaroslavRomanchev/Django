from django.contrib.auth.models import User # импортируем табличку User
from .models import Profile # импортируем табличку Profile
from django.db.models.signals import post_save # сохранение в базу данных 
from django.dispatch import receiver # получатель

@receiver(post_save, sender=User) # Если табличка User что то сохраняет мы ловим сигнал
def create_profile(sender, instance, created, **kwargs): #берем параметры из post_save такие как sender - табличку, instance - та самая табличка которую добавляем, created - данные о создании(создаем или обновляем), и другие возмодных данные в словаре
    if created: # если создаем (юзера)
        Profile.objects.create(user = instance) # добавляем его в табличку Profile

@receiver(post_save, sender=User) 
def save_profile(sender, instance, **kwargs): 
    instance.profile.save() # в любом случае все сохраняем 