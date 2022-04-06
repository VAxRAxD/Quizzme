from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
class createuserform(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'email', 'password1', 'password2'] 
 
class addQuestionform(ModelForm):
    class Meta:
        model=Question
        fields="__all__"
        exclude=("quizname",)