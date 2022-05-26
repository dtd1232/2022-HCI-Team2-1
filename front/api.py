from django.urls import path, include
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
from front.models import Score


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = ['exercise_history', 'score']


# ViewSets define the view behavior.
class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    # permission_classes =


router = routers.DefaultRouter()
router.register(r'scores', ScoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
