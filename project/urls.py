from django.contrib import admin
from django.urls import path, include
from users import views as userViews
from django.contrib.auth import  views as authViews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/', userViews.register, name='reg'),
    path('profile/', userViews.profile, name='profile'),
    path('user/', authViews.LoginView.as_view(template_name='users/user.html'), name='user'), # создаем страницу авторизации
    path('exit/', userViews.custom_logout, name='exit'), # создаем страницу выхода
    path('', include('app.urls')), 
    # Обезательнй ссылки которые должны присуствовать при удалении пароля
    path('pass-reset/', authViews.PasswordResetView.as_view(template_name='users/pass-reset.html'), name='pass-reset'),# страница для удаление пароля (замены)
    path('password_reset_confirm/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'), # эта страничка нужна для поиска по электронной почте пользователя 
    path('password_reset/done/', authViews.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'), # Страничка об успешном обновлении пароля
    path('password_reset_complete/', authViews.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'), # страничка которая нужна чтобы сообщить что пароль был заменен на новый

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    