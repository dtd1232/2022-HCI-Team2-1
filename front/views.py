import math
import time

from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.http import HttpResponseRedirect

from front.models import Exercise, ExerciseHistory


class LogoutView(BaseLogoutView):
    template_name = None

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('login'))


class Register(FormView):
    template_name = 'account/register.html'
    form_class = UserCreationForm


class Play(LoginRequiredMixin, DetailView):
    template_name = 'playing.html'
    queryset = Exercise.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercise_history'] = ExerciseHistory.objects.create(
            exercise=self.object,
            user=self.request.user,
            final_score=0
        )
        return context


class Selection(LoginRequiredMixin, ListView):
    template_name = 'selection.html'
    queryset = Exercise.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ResultView(LoginRequiredMixin, DetailView):
    template_name = 'result.html'
    queryset = Exercise.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exercise_history = ExerciseHistory.objects.filter(
            exercise=self.object,
            user=self.request.user
        ).latest('id')
        exercise_history.end = timezone.now()
        scores = exercise_history.scores.all()
        try:
            average = math.ceil(sum([s.score for s in scores]) / scores.count())
        except ZeroDivisionError:
            average = 0
        exercise_history.final_score = average

        exercise_history.save()
        count_bad = scores.filter(score__lte=84).count()
        count_good = scores.filter(score__gte=85, score__lt=89).count()
        count_perfect = scores.filter(score__gte=89).count()

        total_count = scores.count()
        percentage_bad = math.ceil(count_bad / total_count * 100)
        percentage_good = math.ceil(count_good / total_count * 100)
        percentage_perfect = math.ceil(count_perfect / total_count * 100)

        if percentage_bad + percentage_good + percentage_perfect > 100:
            percentage_bad -= percentage_bad + percentage_good + percentage_perfect - 100

        result_message = 'Perfect!'
        if 33 > percentage_perfect >= 27:
            result_message = 'Good!'
        elif percentage_perfect < 27:
            result_message = 'Keep up!'

        td = str(exercise_history.end - exercise_history.start)
        td_times = td.split(':')
        time_display = f'{td_times[1]} minutes {int(float(td_times[2]))} seconds'

        context['time_exercise'] = time_display
        context['exercise_history'] = exercise_history
        context['result_message'] = result_message
        context['percentages'] = [percentage_bad, percentage_good, percentage_perfect]
        # print(type(exercise_history.end - exercise_history.start))
        return context
