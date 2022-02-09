from django.db import transaction
from rest_framework import viewsets, decorators, status
from rest_framework.response import Response

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

    @decorators.action(
        methods=['GET', 'POST'],
        url_path=r'', 
        detail=True
    )
    @transaction.atomic
    def add_pokemon(self,request, pk):
        """Get and create realeted pokemons.
        
        Allowed Methods:

        GET: Requesting a GET method will return a list of related
        pokemons with the given team (idetified by the pk argument)

        POST: In order to create a single pokemon on a team this action
        allows user to POST a single pokemon data, including a 
        list of abilities to create a new pokemon and set the 
        relationship with the current team.

        POST BODY EXAMPLE:
         {
            "name": "charizard",
            "height": 17,
            "weight": 905,
            "abilities": [
                {
                    "name": "blaze"
                },
                {
                    "name": "solar-power"
                }
            ]
        },

        This action view uses the transaction.atomic in order to
        rollback database if an error occours.
        """
        
        data_to_return = None
        status_to_return = status.HTTP_200_OK
        team = core.models.PokemonTeam.objects.get(pk=pk)
        # Conext is need to build HyperLinked serializers
        context = {
            'request': request
        }

        if request.method == 'POST':
            # Use the serializers to validate data
            serialized_team_data = poke_serializers.PokemonTeamSerializer(
                instance=team,
                context=context
            ).data

            # Use the incomming data from the POST
            serialized_pokemon = poke_serializers.PokemonSerializer(
                data=request.data,
                context=context
            )

            serialized_pokemon.is_valid(raise_exception=True)
            # If pokemon is valid, save it
            serialized_pokemon.save()

            # The pokemons urls are needed to add pokemons
            serialized_team_data['pokemons'].append(serialized_pokemon.data['url'])

            # The team serializer ensures that the information is valid
            updated_team = poke_serializers.PokemonTeamSerializer(
                instance=team,
                data=serialized_team_data,
                context=context
            )

            updated_team.is_valid(raise_exception=True)
            updated_team.save()

            # Sets the data to return and the status code
            data_to_return = serialized_pokemon.data
            status_to_return = status.HTTP_201_CREATED

        else:
            # If the method is GET, return a list of related pokemons
            data_to_return = poke_serializers.PokemonSerializer(
                team.pokemons.all(),
                many=True,
                context=context
            ).data
        
        return Response(data_to_return, status=status_to_return)

    @decorators.action(
        methods=['DELETE'], 
        url_path=r'pokemon/(?P<poke_id>\d+)', 
        detail=True
    )
    @transaction.atomic
    def manage_pokemon(self, request, pk, poke_id):
        """Removes a pokemon from a team.

        The pokemons is removed from the relation with the
        team, it is not deleted from de database, if you want 
        to delete the pokemon, use the pokemon endpoint.
        """
        team = core.models.PokemonTeam.objects.get(pk=pk)
        pokemon = core.models.Pokemon.objects.get(pk=poke_id)
        team.pokemons.remove(pokemon)

        return Response(status=status.HTTP_204_NO_CONTENT)
