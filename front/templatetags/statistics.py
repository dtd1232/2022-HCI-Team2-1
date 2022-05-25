from django import template
from django.db.models import Max

from front.models import ExerciseHistory

register = template.Library()


@register.filter(name='get_play_count')
def get_play_count(exercise, user):
    return ExerciseHistory.objects.filter(
        exercise=exercise,
        user=user
    ).count()


@register.filter(name='get_last_score')
def get_last_score(exercise, user):
    try:
        return ExerciseHistory.objects.filter(
            exercise=exercise,
            user=user
        ).latest('end').final_score
    except ExerciseHistory.DoesNotExist:
        return '-'


@register.filter(name='get_best_score')
def get_best_score(exercise, user):
    best_score = ExerciseHistory.objects.filter(
        exercise=exercise,
        user=user
    ).aggregate(Max('final_score'))['final_score__max']

    return best_score or '-'
