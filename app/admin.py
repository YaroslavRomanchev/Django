from django.contrib import admin
from .models import News
# Register your models here.
# Служит для регистрации моделей, чтобы все те табличи которые мы создали отображались в административке

admin.site.register(News) # регистрируем табличку News