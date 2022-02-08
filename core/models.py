from pyexpat import model
from django.db import models

class PokemonTrainer(models.Model):
    name = models.CharField('Trainer name', max_length=60)
    hometown = models.CharField('Hometown', max_length=20)


class Pokemon(models.Model):
    name = models.CharField('Pokemon name', max_length=60)
    height = models.PositiveIntegerField()
    weight = models.PositiveBigIntegerField()


class Ability(models.Model):
    name = models.CharField(max_length=60)
    pokemon = models.ForeignKey(
        'Pokemon', 
        related_name='abilities', 
        on_delete=models.CASCADE
    )


class PokemonTeam(models.Model):
    owner = models.ForeignKey(
        'PokemonTrainer', 
        related_name='teams', 
        on_delete=models.CASCADE
    )

    pokemons = models.ManyToManyField('Pokemon', related_name='teams') 
