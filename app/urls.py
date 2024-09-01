from django.urls import path
# from views import home

from . import views # импортируем . - из этого же котолога в котором находимся


# Этот файл отслеживает ссылки второго уровня  http://2281337/1_уровень/2уровень/
urlpatterns = [
    path('', views.ShowNewsView.as_view(), name='app_home'), # name - это служит ссылкой на страничку, позже мы ее сможем где то указать например <a href=blog_name></a> 
    path('news/add/', views.CreateNewsView.as_view(), name='news-add'), # страница для создание новой статьи
    path('contacts/', views.contacnts, name = 'contacts'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'), # <В этих скобках пишутся динамичные значения>, int мы указали потому что знаем что там всегда будет числовое значение 
    path('news/<str:username>/', views.UserAllNewsView.as_view(), name='user-news'), # Страница с статьями определенного автора
    path('news/<int:pk>/update/', views.UpdateNewsView.as_view(), name='news-update'), # Страница для обновление статьи
    path('news/<int:pk>/delete', views.DeleteNewsView.as_view(), name='news-delete'), # Страница для удаление статьи
]