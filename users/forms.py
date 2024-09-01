from django import forms
from django.contrib.auth.models import User # базовая модель(встроенная)
from django.contrib.auth.forms import UserCreationForm # базовая форма(встроенная)
from .models import Profile

class UserOurRegistration(UserCreationForm):
    email = forms.EmailField(required=True) # required - важность, обезательное ли поле для заполнения или нет

    class Meta: # это нужно чтобы расположить наше поле email
        model = User    
        fields = ['username', 'email','password1', 'password2', ]


class UserUpdateForm(forms.ModelForm): # форма для изменения username и email
    email = forms.EmailField(required=True) 
# В модели Django, класс Meta используется для определения дополнительных настроек,
#  таких как имя таблицы в базе данных, порядок сортировки, связанные модели и т.д.
    class Meta: 
        model = User    
        fields = ['username', 'email']

class ProfileImage(forms.ModelForm): # форма для изменения изображения
    # это сделано для переименования из img в Изображение профиля
    def __init__(self, *args, **kwards):
        super(ProfileImage, self).__init__(*args, **kwards) # родительский класс
        self.fields['img'].label = 'Изображение профиля' # здесь ставим метку на label 
    class Meta: 
        model = Profile    
        fields = ['img']