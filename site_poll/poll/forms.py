from django.forms import ModelForm
from django import forms
from .models import User, Poll
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RegisterUserForm(forms.ModelForm):
    # username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, error_messages={
        'required': 'Обязательное поле'
    })
    password2 = forms.CharField(label='Пароль повторно', widget=forms.PasswordInput, error_messages={
        'required': 'Обязательное поле'
    })

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError({
                'password2': ValidationError('Введенные пароли не совпадают', code='password_missmatch')
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'fio', 'gender', 'birth_date', 'avatar')






class CustomUserCreationForm(UserCreationForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, error_messages={
        'required': 'Обязательное поле'
    })
    password2 = forms.CharField(label='Пароль повторно', widget=forms.PasswordInput, error_messages={
        'required': 'Обязательное поле'
    })



    class Meta:
        model = User
        fields = ('username', 'fio', 'gender', 'birth_date')



class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'fio', 'gender', 'birth_date')


class CreatePollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'option_one', 'option_two', 'option_three']


