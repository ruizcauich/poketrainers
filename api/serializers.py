from rest_framework import serializers

import core.models


class TrainerSerializer(serializers.HyperlinkedModelSerializer):
    """Serialize the PokemonTrainer model.
    """

    class Meta:
        model = core.models.PokemonTrainer
        fields = ('url', 'name', 'hometown')


class AbilitySerializer(serializers.ModelSerializer):
    """Serialize the pokemon Ability model.
    
    This serializer is not intended to be used directly
    by a view API.
    """
    
    class Meta:
        model = core.models.Ability
        fields = ('name',)


class PokemonSerializer(serializers.ModelSerializer):
    """Serialize the Pokemon model.

    The Ability model has a relationship of many-to-one with
    the Pokemon model, this serializer resolve this relationship
    as a nested list of ablities.
    """

    abilities = AbilitySerializer(many=True)
    class Meta:
        model = core.models.Pokemon
        fields = ('url', 'id', 'name', 'height', 'weight', 'abilities')


class PokemonTeamSerializer(serializers.HyperlinkedModelSerializer):
    """Serialize the PokemonTeam model.

    There is a POKEMON_LIMIT that defines how many pokemon are
    allowed.
    """

    POKEMON_LIMIT = 6
    
    class Meta:
        model = core.models.PokemonTeam
        fields = ('url', 'owner', 'pokemons')
        extra_kwargs={
            'pokemons': {
                'required': False,
            }
        }
    
    def validate_pokemons(self, value):
        """Validates if the amount of pokemons are within the limit.
        """
        # Value is a list
        if len(value) > PokemonTeamSerializer.POKEMON_LIMIT:
            raise serializers.ValidationError(
                f'Teams are limited to a maximum of {PokemonTeamSerializer.POKEMON_LIMIT} pokemon.'
            )
        return value
