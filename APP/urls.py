from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('addQuiz/info/',views.addQuizInfo,name="addQuizInfo"),
    path('addQuiz/<user>/<id>/addQuestions/<number>',views.addQuizQuestion,name="addQuizQuestion"),
    path('quiz/<user>/<id>',views.displayQuiz,name="displayQuiz"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('userquizes/',views.getUserQuiz,name="quizes"),
    path('enterquiz/',views.enterQuizLink,name='enterquiz')
]