from captcha.fields import CaptchaField, CaptchaTextInput
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Responds, Comment, IsPassedTest
from django import forms
from django.forms import ModelForm, TextInput, CheckboxInput, FileInput


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'quests/custom_captcha.html'


class IsPassedForm(ModelForm):

    widgets = {
        'TestID': TextInput(attrs={'class': 'form-control'}),
        'UserID': TextInput(attrs={'class': 'form-control'}),
        'IsPassed': TextInput(attrs={'class': 'form-control'})
    }

    class Meta:
        model = IsPassedTest
        fields = ['TestID', 'UserID', 'IsPassed']


class CommentForm(ModelForm):

    text = forms.CharField(label="Комментарий", widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'Комментарий'}))
    captcha = CaptchaField(widget=CustomCaptchaTextInput)

    widgets = {
        'UserID': TextInput(attrs={'class': 'form-control'}),
    }

    class Meta:
        model = Comment
        fields = ['UserID', 'text']


class RespondTestForm(ModelForm):
    # QuestionID = forms.CharField(label="Вопрос", widget=forms.TextInput(attrs={'class': 'form-control'}))
    # Answer = forms.CharField(label='Ответ', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ответ'}))
    widgets = {

        "QuestionID": TextInput(attrs={"placeholder": "Вопрос", "class": "form-control"}),
        "UserId": TextInput(attrs={"placeholder": "Пользователь", "class": "form-control"}),
        'Answer': TextInput(attrs={'placeholder': 'Ответ', 'class': 'form-control'}),
        'VideoAnswer': FileInput(attrs={'class': 'form-file-input'})

    }

    class Meta:
        model = Responds
        fields = ["QuestionID", "Answer", "UserId", 'VideoAnswer']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(widget=CustomCaptchaTextInput)


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(widget=CustomCaptchaTextInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')