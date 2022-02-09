import logging
from django.test import TestCase

from .models import PokemonTrainer, PokemonTeam


logger = logging.getLogger(__name__)

class PokemonTrainerTest(TestCase):

    def setUp(self):
        logger.debug("Setting up PokemonTrainerTest")

        PokemonTrainer.objects.create(
            name='Ash ketchum',
            hometown='Pallet Town')

    
    def test_not_foud_trainer(self):
        """Tests that a Trainer object is not found.
        """
        logger.debug("Execuiting test_not_foud_trainer")

        with self.assertRaises(PokemonTrainer.DoesNotExist):
            PokemonTrainer.objects.get(id=10)

    def test_str_pokemontrainer(self):
        """Tests the str method.
        """
        logger.debug("Execuiting test_str_pokemontrainer")

        trainer = PokemonTrainer.objects.first()
        self.assertEqual("Ash ketchum from Pallet Town", str(trainer))


class PokemonTrainerPokemonTeamTest(TestCase):

    def setUp(self):
        logger.debug("Setting up PokemonTrainerPokemonTeamTest")

        trainer = PokemonTrainer.objects.create(
            name='Ash ketchum',
            hometown='Pallet Town')

        PokemonTeam.objects.create(owner=trainer)
        PokemonTeam.objects.create(owner=trainer)

    def test_trainer_has_two_teams(self):
        logger.debug("Execuiting test_trainer_has_two_teams")

        trainer = PokemonTrainer.objects.first()

        self.assertEquals(2,trainer.teams.all().count())
