from statistics import mode
from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name

class Attempts(models.Model):
    examinee=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    quizname=models.ForeignKey(Quiz,null=True,on_delete=models.CASCADE)

class Result(models.Model):
    quizname=models.ForeignKey(Quiz,null=True,on_delete=models.CASCADE)
    student=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    marks=models.IntegerField(null=True)

    def __str__(self):
        return f"{self.student.username} {self.quizname} {self.marks}"

class Question(models.Model):
    quizname=models.ForeignKey(Quiz,null=True,on_delete=models.CASCADE)
    question = models.CharField(max_length=200,null=True)
    option_1 = models.CharField(max_length=200,null=True)
    option_2 = models.CharField(max_length=200,null=True)
    option_3 = models.CharField(max_length=200,null=True)
    option_4 = models.CharField(max_length=200,null=True)
    answer = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.question

