from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html' # use our existing "polls/index.html" template.
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return Question.objects.order_by('-pubpublished_date')[:5] #bug

        # returns a queryset containing Questions whose pub_date is less than or equal to - that is, earlier than or equal to - timezone.now.
        return Question.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:5] 


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html' # uses the template "polls/question_detail.html"
    
    def get_queryset(self):
        return Question.objects.filter(published_date__lte=timezone.now()) # lte = less than or equal to


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    def get_queryset(self):
        return Question.objects.filter(published_date__lte=timezone.now()) # lte = less than or equal to


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


""" def index(request):
    latest_question_list = Question.objects.order_by('-published_date')[:5]
    context = {'latest_question_list': latest_question_list,}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice']) 
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id))) """