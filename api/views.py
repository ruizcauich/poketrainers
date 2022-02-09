from rest_framework import viewsets

import core.models
from . import serializers as poke_serializers


class TrainerViewSet(viewsets.ModelViewSet):
    serializer_class = poke_serializers.TrainerSerializer
    queryset = core.models.PokemonTrainer.objects.all()


class PokemonViewSet(viewsets.ModelViewSet):
    serializer_class = poke_serializers.PokemonSerializer
    queryset = core.models.Pokemon.objects.all()


class PokemonTeamViewSet(viewsets.ModelViewSet):
    serializer_class = poke_serializers.PokemonTeamSerializer
    queryset = core.models.PokemonTeam.objects.all()
