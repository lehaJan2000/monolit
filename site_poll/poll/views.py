from datetime import datetime

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseForbidden

from django.contrib import auth
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import RegisterUserForm, CreatePollForm
from .models import Poll
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

User = get_user_model()


# Create your views here.
def index(request):
    time_threshold = timezone.now() - timedelta(minutes=1)
    polls = Poll.objects.filter(startpoll__gt=time_threshold)

    context = {
        'polls': polls
    }
    return render(request, 'main/index.html', context)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Такой страницы не существует</h1>")


class BBLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.pk])


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm

    def get_success_url(self):
        return reverse_lazy('login')


@login_required
def profile(request, id):
    user = User.objects.get(id=id)
    time_threshold = timezone.now() - timedelta(minutes=1)
    polls = Poll.objects.filter(startpoll__gt=time_threshold, user=user)

    context = {
        'polls': polls,
        'user': user
    }
    return render(request, 'main/profile.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def delete_profile(request):
    user = get_object_or_404(User, id=request.user.id)
    if request.user == user:
        user.delete()
        return redirect('index')
    else:
        return HttpResponseForbidden("ты не можешь его удалить лох")


@login_required
def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            # print(form.cleaned_data['question'])
            return redirect('index')
    else:
        form = CreatePollForm()
    context = {
        'form': form
    }
    return render(request, 'main/create.html', context)


@login_required
def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form')

        poll.save()

        return redirect('results', poll.id)

    context = {
        'poll': poll
    }
    return render(request, 'main/vote.html', context)


@login_required
def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    total_votes = poll.option_one_count + poll.option_two_count + poll.option_three_count

    if total_votes == 0:
        option_one_percentage = option_two_percentage = option_three_percentage = 0
    else:
        option_one_percentage = (poll.option_one_count / total_votes) * 100
        option_two_percentage = (poll.option_two_count / total_votes) * 100
        option_three_percentage = (poll.option_three_count / total_votes) * 100

    return render(request, 'main/results.html', {
        'poll': poll,
        'total_votes': total_votes,
        'option_one_percentage': option_one_percentage,
        'option_two_percentage': option_two_percentage,
        'option_three_percentage': option_three_percentage,
    })


@login_required
def delete_poll(request):
    polls = Poll.objects.all()
    context = {
        'polls': polls
    }
    return render(request, 'main/delete_poll.html', context)
