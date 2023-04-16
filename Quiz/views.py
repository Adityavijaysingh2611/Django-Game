from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.template import loader
from .forms import *
from .models import *
from django.http import HttpResponse
import operator

# Create your views here.
def home(request):
    if request.user.is_staff:
        return redirect('adminHome')
    
    if request.method == 'POST':
        print(request.POST)
        questions=QuesModel.objects.all()
        score=0
        wrong=0
        correct=0
        total=0
        for q in questions:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = score/(total*10) *100
        
        buttonShow=True
        if percent > 75:
            buttonShow = False
        
        context = {
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total,
            'buttonShow':buttonShow
        }

        if request.user.is_authenticated:
            statistics=Stats(request.POST)
            Stats.objects.create(
                name = request.user.username,
                time = request.POST.get('timer'),
                score = score
            )
        else:
            statistics=Stats(request.POST)
            Stats.objects.create(
                name = "AnonymousUser",
                time = request.POST.get('timer'),
                score = score
            )


        return render(request,'Quiz/result.html',context)
    else:
        questions=QuesModel.objects.all()
        context = {
            'questions':questions
        }
        return render(request,'Quiz/home.html',context)

def addQuestion(request):    
    if request.user.is_staff:
        form=addQuestionform()
        if(request.method=='POST'):
            form=addQuestionform(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        context={'form':form}
        return render(request,'Quiz/addQuestion.html',context)
    else: 
        return redirect('home') 

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home') 
    else: 
        form=createuserform()
        if request.method=='POST':
            form=createuserform(request.POST)
            if form.is_valid() :
                user=form.save()
                return redirect('login')
        context={
            'form':form,
        }
        return render(request,'Quiz/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
       context={}
       return render(request,'Quiz/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('/')

def adminHome(request):
    all_users = Stats.objects.values()

    sorted_users = Stats.objects.all().order_by('-score').values()
    print(sorted_users)

    count=0

    for i in all_users:
        count=count+1

    print(count)

    user_names=[]
    id=[]
    # for i in all_users:
    #     user_names.append(i["username"])
    #     id.append(i["score"])

    #print(all_users)

    #print(all_users[0]["username"])
    context={
        'users':all_users,
        'sorted':sorted_users,
        'count':count
    }
    #context={all_users}
    return render(request,'Quiz/adminHome.html',context)

