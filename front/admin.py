from django.contrib import admin

# Register your models here.
from front.models import Exercise, ExerciseHistory, Score


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ExerciseHistory)
class ExerciseHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise', 'final_score', 'start', 'end']
    fields = ['user', 'exercise', 'final_score', 'start', 'end']
    readonly_fields = ['user', 'exercise', 'final_score', 'start', 'end']


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['exercise_history', 'score', 'created']
