import email
from django.shortcuts import render,redirect
from django.forms import formset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import *
from .forms import *
from .authenticators import *
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@unauthenticated_user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'html/login.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@unauthenticated_user
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = createuserform()
        if request.method == 'POST':
            form = createuserform(request.POST)
            if form.is_valid():
                user = form.save()
                username = user.username
                messages.success(request, 'Account was created for ' + username)
                return redirect('login')
        context = {'form': form}
        return render(request, 'html/register.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutUser(request):
    logout(request)
    return redirect('login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def home(request):
    return render(request,'html/home.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def addQuizInfo(request):
    if request.method=='POST':
        questions=request.POST.get('questions')
        name=request.POST.get('name')
        user=request.user
        quiz=Quiz.objects.create(
            user=user,
            name=name
        )
        return redirect("addQuizQuestion",user=request.user.id,id=quiz.id,number=questions)
    return render(request, 'html/addQuizInfo.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def addQuizQuestion(request,user,id,number):
    QuestionFormSet = formset_factory(addQuestionform, extra=int(number))
    quiz=Quiz.objects.get(id=id)
    formset=QuestionFormSet()
    if request.method == 'POST':
        formset = QuestionFormSet(request.POST)
        data=dict(formset.data)
        data.pop('csrfmiddlewaretoken')
        for i in range(int(number)):
            question=data['form-'+str(i)+'-question'][0]
            option_1=data['form-'+str(i)+'-option_1'][0]
            option_2=data['form-'+str(i)+'-option_2'][0]
            option_3=data['form-'+str(i)+'-option_3'][0]
            option_4=data['form-'+str(i)+'-option_4'][0]
            answer=data['form-'+str(i)+'-answer'][0]
            Question.objects.create(
                quizname=quiz,
                question=question,
                option_1=option_1,
                option_2=option_2,
                option_3=option_3,
                option_4=option_4,
                answer=answer
            )
        messages.success(request, 'Quiz created sucessfully. Visit '+'http://127.0.0.1:8000/quiz/'+str(user)+'/'+str(quiz.id))
        return redirect('/')
    context = {'formset': formset}
    return render(request, 'html/addQuizQuestion.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def displayQuiz(request,user,id):
    owner=User.objects.get(id=user)
    quiz=Quiz.objects.get(id=id)
    if request.user!=owner:
        try:
            attempt=Attempts.objects.filter(examinee=request.user,quizname=quiz)[0]
            result=Result.objects.filter(quizname=id,student=request.user.id)[0]
            context={'marks':result.marks}
            return render(request, 'html/result.html',context)
        except:
            pass
    questions=Question.objects.filter(quizname=id)
    if request.method=="POST":
        correct=0
        for q in questions:
            if q.answer==request.POST.get(q.question):
                correct+=1
        if request.user!=owner:
            Result.objects.create(
                quizname=quiz,
                student=request.user,
                marks=correct
            )
            Attempts.objects.create(
                examinee=request.user,
                quizname=quiz
            )
        return redirect('home')
    context={'questions':questions,'owner':owner}
    return render(request,'html/quizPage.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def getUserQuiz(request):
    user=request.user
    quizes=Quiz.objects.filter(user=user)
    id=[quiz.id for quiz in quizes]
    results=Result.objects.filter(quizname_id__in=id)
    context={'quizes':quizes,'results':results}
    return render(request,'html/quizes.html',context)

def enterQuizLink(request):
    if request.method=="POST":
        link=request.POST.get('link')
        userid=(link.split('/'))[-2]
        quizid=(link.split('/'))[-1]
        return redirect("displayQuiz",user=userid,id=quizid)
    context={}
    return render(request,'html/enterquiz.html',context)