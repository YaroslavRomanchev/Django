from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404 # для предоставления статей пользователя импортируем get_object_or_404
from django.contrib.auth.models import User # Импорт таблички, для предоставления статей пользователя
# Функция render позволяет вывести что либо на экран
# СreateView - класс который позволяет что то создавать на сайте, в нашем случае статьи
from django.views.generic import ( # generic - библиотека отвещающая за списки и массивы, DetailViews - позволяет работать с лишь одним объектом
    # Эти классы много где нужны, в общем они нужны для работы  с списками и другими вещами
    ListView,  # Оно предоставляет множество полезных функций прямо "из коробки", облегчая создание страниц, где нужно показать набор элементов 
    DetailView, 
    CreateView,
    UpdateView, # Позволяет обновлять все данные
    DeleteView, # удаляет статьи

    
) 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import News

#_______________________________________________________________________________________________


# request - запрос, обезательный параметр
def home(request): # для отображения данных
    data = {
        'news' : News.objects.all(), # говорим что берем каждый объект из базы данных
        'title': 'Главная страница приложения'
    }
    # подключаем шаблонизатор
    return render(request, 'app/home.html', data) # запрос, шаблон, то что передаемЫ

#_______________________________________________________________________________________________

def contacnts(request):
    return render(request, 'app/contacts.html', {'title': 'Страничка про нас'}) # можно передавать сразу здесь же создавая словарик

#_______________________________________________________________________________________________
# Все это нужно для отображения статей
class ShowNewsView(ListView): # название фукнции наше, наследуем от ListView

    model = News #title, text, date, avtor
    template_name = 'app/home.html' # шаблон  с которым мы будем работать
    context_object_name = 'news' # объект по которому проходимся типо, по умолчанию там стоит objects
    ordering = ['-date'] # сортирует все в другом порядке(сверху новые снизу старые статьи) статьи
    paginate_by = 5 # сколько статей должно быть на странице(home.html)
    
    def get_context_data(self, **kwargs): # еще добавляем данные (хотя можно было сделать проще)
        ctx = super(ShowNewsView, self).get_context_data(**kwargs) # получаем доступ ко всем файлам через родителя
        ctx['title'] = 'Главная страница приложения'# добавляем новое значение
        #можем добавить еще кучу
        return ctx
    
#_______________________________________________________________________________________________

class NewsDetailView(DetailView): #            
    model = News #                           title, text, date, avtor
    template_name = 'app/news_detail.html' # так то это стоит по умолчанию поэтому можно не писать
    # context_object_name = 'post'           мы могли так написать но не стоит(просто укажем новое имя в шаблоне)
    
    def get_context_data(self, **kwargs): # еще добавляем данные (хотя можно было сделать проще)
        ctx = super(NewsDetailView, self).get_context_data(**kwargs) # получаем доступ ко всем файлам через родителя
        ctx['title'] = News.objects.filter(pk=self.kwargs['pk']).first()# filter - это функция для чего то определенного(фильтрует), 
        # так как статья первая пишется пишем first()
        #можем добавить еще кучу
        return ctx


#_______________________________________________________________________________________________
# Этот класс нужен чтобы создавать статьи
# Здесь стоит шаблон(template_name) по умолчанию - news_form
# С помощью LoginRequiredMixin мы не сможет зайти на страницу для добавление статьи, если не авторизованы

class CreateNewsView(LoginRequiredMixin, CreateView):
    model = News
    fields = ['title', 'text']
    
    # При нажатии кнокпи(добавить статью) будет вызываться данная функция
    def form_valid(self, form): 
        form.instance.avtor = self.request.user # Эта строка кода присваивает текущего авторизованного пользователя 
        # (доступного через self.request.user) в поле avtor модели News
        return super().form_valid(form) # Этот вызов выполняет стандартную обработку формы, обеспечиваемую методом
        # form_valid в родительском классе (CreateView). Он сохраняет форму и делает перенаправление на страницу 
        # по умолчанию, обычно это get_success_url()
    
    

#_______________________________________________________________________________________________
# Этот класс нужен чтобы обновить статью
# С помощью UserPassesTestMixin не даем обновлять статью левым людям(а только авторам статьи)
class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    fields = ['title', 'text']
    
    # При нажатии кнокпи(добавить статью) будет вызываться данная функция
    def form_valid(self, form): 
        form.instance.avtor = self.request.user
        return super().form_valid(form)
    
    # Проверка на обновление статьи(кто обновляет левый чел или автор статьи?)
    def test_func(self):
        news = self.get_object()
        if self.request.user == news.avtor:
            return True
        return False

#_______________________________________________________________________________________________
# Удаляет статьи
# Достаточно создать данный класс и шаблон к нему, и в шаблоне сделать форму с кнопкой, и все будет работать
#  Ну и конечно чтобы проверка прошла, на права и аунтефикацию
class DeleteNewsView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    success_url = '/' # при успешном удалении нас перекинут на гл. страничку
    
    # Проверка на обновление статьи(кто обновляет левый чел или автор статьи?)
    def test_func(self):
        news = self.get_object()
        if self.request.user == news.avtor:
            return True
        return False
    

#_______________________________________________________________________________________________
# Для показа статьи пользователя
class UserAllNewsView(ListView): # название фукнции наше, наследуем от ListView

    model = News #title, text, date, avtor
    template_name = 'app/user_news.html' # шаблон  с которым мы будем работать
    context_object_name = 'news' # объект по которому проходимся типо, по умолчанию там стоит objects
    paginate_by = 5 # сколько статей должно быть на странице(home.html)

    def get_queryset(self): # именно эта функция(нужная для вывода определенных статей)
        user = get_object_or_404(User, username=self.kwargs.get('username')) # из адреса получаем имя пользователя(автора статьи)
        return News.objects.filter(avtor=user).order_by('-date') # Возвращает именно его статьи
    
    def get_context_data(self, **kwargs): # еще добавляем данные (хотя можно было сделать проще)
        ctx = super(UserAllNewsView, self).get_context_data(**kwargs) # получаем доступ ко всем файлам через родителя
        ctx['title'] = f"Все статьи от пользователя: {self.kwargs.get('username')}"# добавляем новое значение
        #можем добавить еще кучу
        return ctx
    