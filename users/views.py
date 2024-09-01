from django.shortcuts import render, redirect # redirect - переадресация на другую страничку
from .forms import UserOurRegistration, UserUpdateForm, ProfileImage # форма для регистрации
from django.contrib import messages # для вывода сообщений
from django.contrib.auth.decorators import login_required # наш декоратор( используется для ограничения доступа
# к определенным представлениям в Django, требуя, чтобы пользователь был аутентифицирован)
from django.contrib.auth import logout # используется для завершения сеанса аутентифицированного пользователя в Django-приложени



# Create your views here.
# Функция для регистрации
def register(request):
    if request.method == 'POST': # если запрос это post
        form = UserOurRegistration(request.POST) # создаем форму уже зопостенную
        if form.is_valid(): # если форма была заполнена правильно
            form.save() # закидываем это в базу данных
            username = form.cleaned_data.get('username') # берем отфильтрованный текст из поля username
            messages.success(request, f'Аккаунт: {username} был успешно создан, введите имя пользователя и пароль для авторизации') # выводим сообщение про пользователя
            return redirect('user') # переходим на страницу входа
    else: # в другом случае
        form = UserOurRegistration() # берем обычную форму
    return render(request, 'users/registration.html', {'form': form, 'title':'Регистрация пользователя'}) # передаем базовую формочку и название страницы 
# на регистрационную страницу

# messages.debug - информация об обкладке
# messages.info - определенная информация
# messages.success - выведется информация когда успешно обработается формачка
# messages.warning = предупреждающее сообщение
# messages.error - будет вызываться когда мы будем получать некую ошибку

# для странички exit.html 
def custom_logout(request):
    logout(request)
    return render(request, 'users/exit.html')



# Эта функция нужна для обновления данных в профиле
@login_required # здесь нужен декоратор чтобы страница с профилем открывалась только тогда когда мы находимся авторизованными
def profile(request):
    if request.method == 'POST': # если запрос это post
        img_profile = ProfileImage(request.POST, request.FILES,instance=request.user.profile) # получаем данные с POST и получаем файлы 
        update_user = UserUpdateForm(request.POST, instance=request.user)# получаем данные с POST

        if update_user.is_valid() and img_profile.is_valid(): # если формочки были правильно заполнены
            update_user.save() # сейвим все в базу данных
            img_profile.save()
            messages.success(request, f'Ваш аккаунт был успешно обновлен') # при успешной обработки формы выводим сообщение
            return redirect('profile')# возвращаем на ту же страницу
    else:# в друго случае просто загружаем формочки уже с нашим профилем и юзером
        img_profile = ProfileImage(instance=request.user.profile)
        update_user = UserUpdateForm(instance=request.user)

    data = {
        'img_profile': img_profile,
        'update_user':update_user
    }

    return render(request, 'users/profile.html', data)



# @receiver(post_save, sender=User) # если что то добавляется, сохраняется в табличку User мы ловим сигнал
# def create_profile(sender, instance, created, **kwargs): #берем параметры из post_save такие как sender - табличку, instance - то что добавляем, created - данные о создании(создаем или нет), и другие возмодных данные в словаре
#     if created: # если создаем (юзера)
#         Profile.objects.create(user = instance)