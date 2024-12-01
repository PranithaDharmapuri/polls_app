import datetime
from django.utils import timezone
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from my_app.models import Question, Choice,User
from django.db.models import F
from my_app.forms import LoginForm,RegisterForm
from django.contrib.auth.models import User

def index(request):
    latest_question_list=Question.objects.order_by("-pub_date")
    # choice_list=Choice.objects.order_by("pk")
    context={
        "latest_question_list": latest_question_list,
        # "choice_list": choice_list
    }
    return render(request,'my_app/index.html',context)

def details(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'my_app/details.html',{"question":question})

def results(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'my_app/results.html',{"question":question})

def vote(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(request,"my_app/details.html",
            {
                "question":question,
                "error_message":"You haven't selected any choice! Please do select first",
            },
        )   
    else:
        print("vote successful")
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        print("vote successful")
        return HttpResponseRedirect(reverse("polls:results",args=(question.id,)))
    
def delete_question(request,question_id):
    question=Question.objects.filter(pk=question_id).delete()
    return redirect('polls:index')

def add_question(request):
    if request.method == 'POST':
        question_text=request.POST.get('question_text')
        choice_text=request.POST.getlist('choice_text')

        if question_text:
            question=Question.objects.create(question_text=question_text,pub_date=timezone.now())
            for values in choice_text:
                Choice.objects.create(question=question,choice_text=values,votes=0)
            question.save()
            return redirect('polls:index')
        else:
            return render(request,'my_app/add_question.html',{
                'error_message':'All fields are required!'
            })
    return render(request,"my_app/add_question.html")

def update_question(request,question_id):
    question=get_object_or_404(Question,id=question_id)

    if request.method == 'POST':
        new_text=request.POST.get('question_text')

        question.question_text=new_text
        question.save()
        return redirect('polls:index')
    return render(request,'my_app/update_question.html',{'question':question})

def thanks(request):
    return render(request,'my_app/thanks.html',{'message':'Thank you for contribution!'})

def login_page(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            try:
                user=User.objects.get(name=name, email=email, password=password)
                return HttpResponse(f"<h1>Welcome, {user.name}!")
            except User.DoesNotExist:
                return HttpResponse("Invalid Login details")
    else:
        form=LoginForm()
    
    return render(request,"my_app/login_page.html",{'form':form})

def add_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()
            return redirect("polls:thanks")
    else:
        form=RegisterForm()

    return render(request,'my_app/add_user.html',{'form':form})
