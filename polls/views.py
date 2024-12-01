from typing import Any
# from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import redirect, render,get_object_or_404
from django.urls import reverse
from django.views import generic
from django.db.models import F

from polls.forms import NameForm

from .models import Choice,Questions,Signup


class IndexView(generic.ListView):
    template_name="polls/index.html"
    context_object_name="latest_question_list"

    def get_queryset(self):
        return Questions.objects.order_by("-pub_date")[:5]
 
class DetailView(generic.DetailView):
    model=Questions
    template_name="polls/detail.html"


class ResultsView(generic.DetailView):
    model=Questions
    template_name="polls/results.html"

def vote(request,question_id):
    question = get_object_or_404(Questions, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request, "polls/detail.html",   
            {
                "object":question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes=F("votes") + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
def update_question(request,question_id):
    question=get_object_or_404(Questions,pk=question_id)
    if request.method == 'POST':
        new_text=request.POST.get('question_text')
        if new_text:
            question.question_text=new_text
            question.save()
        for choice in question.choice_set.all():
            new_choice=request.POST.get(f'choice_{choice.id}')
            print(f'choice_{choice.id}')
            print("123",choice.choice_text)

            if new_choice:
                print(choice)
                choice.choice_text=new_choice
                print("@@@@",choice.choice_text)
                choice.save()
        return redirect(reverse('polls:detail',kwargs={'pk':question.id}))
    return render(request,'polls/update_question.html',{"question":question})

def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse("polls:thanks"))
    else:
        form = NameForm()
    
    return render(request,"polls/signup.html",{"form":form})

def thanks(request):
    return HttpResponse("<h3> Thanks for your Contribution.<h3>")