from django.db import models
from django.conf import settings

from front.utils import FilenameChanger


class Exercise(models.Model):
    CATEGORY_CHOICES = [
        ('workout', 'Workout'),
        ('pilates', 'Pilates'),
        ('yoga', 'Yoga'),
        ('dance', 'Dance'),
    ]

    DIFFICULTY_CHOICES = [
        ('1', 'Easy'),
        ('3', 'Moderate'),
        ('5', 'Hard')
    ]
    name = models.CharField('Name', max_length=100)
    category = models.CharField('Category', choices=CATEGORY_CHOICES, max_length=20)
    preview = models.ImageField('Preview Image', upload_to=FilenameChanger('media/preview/'), null=True)
    # play_count = models.PositiveIntegerField('Play count')
    source = models.FileField('File')
    difficulty = models.CharField('Difficulty', choices=DIFFICULTY_CHOICES, max_length=10)
    star_count = models.PositiveIntegerField('Star count', blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'({self.pk}) {self.name}'

    def save(self, **kwargs):
        self.star_count = int(self.difficulty)
        super().save(**kwargs)

    def get_star_list(self):
        return [i for i in range(0, self.star_count)]



class ExerciseHistory(models.Model):
    exercise = models.ForeignKey(
        'Exercise',
        related_name='exercise_histories',
        on_delete=models.PROTECT,
        verbose_name='Exercise'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='exercise_histories',
        verbose_name='User',
        on_delete=models.CASCADE
    )
    final_score = models.DecimalField('Score', max_digits=5, decimal_places=2)
    start = models.DateTimeField('Start', auto_now_add=True)
    end = models.DateTimeField('End', null=True)


class Score(models.Model):
    exercise_history = models.ForeignKey(
        'ExerciseHistory',
        related_name='scores',
        on_delete=models.CASCADE,
        verbose_name='Exercise History'
    )
    score = models.PositiveIntegerField('Score')
    created = models.DateTimeField('Created', auto_now_add=True)
