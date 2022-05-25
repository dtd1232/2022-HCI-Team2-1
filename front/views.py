from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
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


class Selection(LoginRequiredMixin, ListView):
    template_name = 'selection.html'
    queryset = Exercise.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exercises = self.object_list

        data = {}
        for exercise in exercises:
            data[exercise.id] = {
                'best_score': -1,
                'last_score': -1,
                'play_count': 0
            }

            histories = ExerciseHistory.objects.filter(
                exercise=exercise,
                user=self.request.user
            )
            data[exercise.id]['play_count'] = histories.count()
            best_score = -1
            for history in histories:
                if history.final_score > best_score:
                    best_score = history.final_score

            try:
                last_exercise = ExerciseHistory.objects.filter(
                    exercise=exercise,
                    user=self.request.user
                ).latest('start')

                data[exercise.id]['last_score'] = last_exercise.final_score
            except ExerciseHistory.DoesNotExist:
                data[exercise.id]['last_score'] = 'Not yet done'

            if best_score == -1:
                best_score = 'Not yet done'

            data[exercise.id]['best_score'] = best_score

        context['data'] = data
        context['user'] = self.request.user
        return context
