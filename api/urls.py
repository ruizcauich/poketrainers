from importlib.resources import path

from django.urls import URLPattern
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register('trainers', views.TrainerViewSet)
router.register('pokemon', views.PokemonViewSet)
router.register('teams', views.PokemonTeamViewSet)

urlpatterns = router.urls


