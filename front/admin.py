from django.contrib import admin

# Register your models here.
from front.models import Exercise, ExerciseHistory


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ExerciseHistory)
class ExerciseHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise']

